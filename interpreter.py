from instructions import *
from keyboard import get_keyboard
import argparse
import os
import subprocess
import sys


class Computer:
    def __init__(self, mem_size, verbose):
        self.keyboard = get_keyboard()

        self.registers = [0 for _ in range(16)]
        self.set_reg(14, mem_size * 4)
        self.memory = [0 for _ in range(mem_size * 4)]
        self.flags = {'N': False, 'Z': False, 'C': False, 'O': False}
        self.instruction = Instruction(0)
        self.halted = False
        self.verbose = verbose

    def read_memory_file(self, file):
        with open(file) as input_file:
            # The assembler includes the version as the first line
            machine_code = input_file.readlines()[1:]

        if len(machine_code) * 4 > len(self.memory):
            print('[!] WARNING: Machinecode does not fit in memory!')
            print('[!] Adjusting memory size to fit machinecode...')
            self.memory += [0 for _ in range(len(machine_code) * 4 - len(self.memory))]
            self.set_reg(14, len(self.memory))

        for address, instruction in enumerate(machine_code):
            data = int(instruction.strip(), 16)

            self.write_memory(4 * address, data)

    def print_memory(self):
        print('\n' + '-'*44)
        for i in range(0, len(self.memory), 4):
            print(('| 0x{:08x}  | ' + ' 0x{:02x} |' * 4).format(
                i,
                self.memory[i], self.memory[i + 1],
                self.memory[i + 2], self.memory[i + 3])
            )
        print('-' * 44)

    def print_registers(self):
        for i in range(16):
            print('R{:<2d} = 0x{:08x} ({:d})'.format(i, self.registers[i], self.registers[i]))

    def get_reg(self, reg):
        return self.registers[reg]

    def set_reg(self, reg, value):
        if reg > 0:
            self.registers[reg] = value

    def assert_valid_address(self, address):
        if address & 3:
            print('\n[!] Invalid memory address: 0x{:08x}'.format(address))
            print('[!] Shutting down processor...')
            self.halt()
            return False
        elif address + 3 >= len(self.memory):
            print('\n[!] Memory address out of range: 0x{:08x}'.format(address))
            print('[!] Shutting down processor...')
            self.halt()
            return False
        return True

    def read_memory(self, address):
        if not self.assert_valid_address(address):
            return

        if address == -512:
            data = self.keyboard.read_character()
        else:
            data = (self.memory[address] << 24) + (self.memory[address + 1] << 16)
            data += (self.memory[address + 2] << 8) + (self.memory[address + 3])

        return data

    def write_memory(self, address, data):
        if not self.assert_valid_address(address):
            return

        if address == -512:
            if self.is_verbose():
                print('\n[!] Output: {}\n'.format(chr(data)))
            else:
                sys.stdout.write(chr(data))
                sys.stdout.flush()
        else:
            self.memory[address] = (data >> 24) & 0xff
            self.memory[address + 1] = (data >> 16) & 0xff
            self.memory[address + 2] = (data >> 8) & 0xff
            self.memory[address + 3] = data & 0xff

    def set_flags(self, n, z, c, o):
        self.flags['N'] = n
        self.flags['Z'] = z
        self.flags['C'] = c
        self.flags['O'] = o

    def fetch(self):
        pc = self.get_reg(15)
        instr = self.read_memory(pc)

        if instr < 16:
            print('\n[!] Useless operation OR 0, R0, R0 found.')
            print('[!] Did you forget to include a HALT instruction?')
            print('[!] Shutting down processor...')
            self.halt()
            return

        self.instruction = get_instruction(instr)
        self.set_reg(15, pc + 4)

    def test(self):
        cond = self.instruction.get_condition()
        neg = cond & 1
        cond >>= 1
        n, z, c, o = (self.flags['N'], self.flags['Z'],
                      self.flags['C'], self.flags['O'])

        conditions = (z, c, n, o, c and not z, n == o, n == o and not z, False)

        if neg:
            return not conditions[cond]
        else:
            return conditions[cond]

    def execute(self):
        self.instruction.execute(self)

    def run(self):
        while not self.halted:
            self.fetch()
            if not self.test():
                continue

            if self.is_verbose():
                print(str(self.instruction))
            self.execute()

    def halt(self):
        self.halted = True

    def is_verbose(self):
        return self.verbose


def get_assembler():
    if sys.platform.startswith('linux'):
        return 'bin/linux/assembler'
    elif sys.platform == 'darwin':
        return 'bin/macos/assembler'
    else:
        return 'bin/windows/assembler.exe'


parser = argparse.ArgumentParser(description="""
Interpreter for the machinecode of the RUN1920 CPU, by the Radboud University
Nijmegen.
Based on assembly and machinecode by David N. Jansen.
""")

parser.add_argument('filename', help='The filename of the machinecode')
parser.add_argument('-m', '--memory', default=2**10, type=int,
                    help='The size of the RAM in 4-byte words (default=1024)')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Print the executed assembly instructions')
parser.add_argument('-sm', '--show-memory', action='store_true',
                    help='Print the RAM memory after execution')
parser.add_argument('-sr', '--show-registers', action='store_true',
                    help='Print the registers after execution')
parser.add_argument('-a', '--assemble', action='store_true',
                    help='Assemble the inputfile first (requires assembler)')

args = parser.parse_args()

if not os.path.exists(args.filename):
    print('[!] File {} not found!'.format(args.filename))
    exit()

if args.assemble:
    asm = get_assembler()

    if not os.path.exists(asm):
        print('[!] Assembler ({}) not found!'.format(asm))
        exit()

    p = subprocess.Popen([asm, args.filename], stderr=subprocess.PIPE)
    _, err = p.communicate()

    if p.returncode != 0:
        print(err.decode('utf-8'))
        exit()

    print('[!] File assembled successfully!')

    filename = os.path.splitext(args.filename)[0] + '.hex'
else:
    filename = args.filename

cmp = Computer(args.memory, args.verbose)
cmp.read_memory_file(filename)

try:
    cmp.run()
except KeyboardInterrupt:
    print('[!] Processor interrupted!')
    cmp.halt()

if args.show_memory:
    cmp.print_memory()

if args.show_registers:
    cmp.print_registers()
