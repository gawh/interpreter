
Interpreter for the machinecode of the RUN1920 CPU, by the Radboud University Nijmegen. Based on assembly and machinecode by David N. Jansen.

Interpreter source code can be found on [GitHub](https://github.com/gijshendriksen/interpreter/).

Requirements
------------

Python 2 or 3


Usage
-----

In a Windows command prompt, or a Linux/MacOSX terminal, enter the following command:

    python interpeter.py filename

For example:  `python interpreter.py example.hex`  reads the contents of the file "example.hex" as machinecode, and executes it.


Flags
-----

There are multiple flags that can be used to execute this program:

    -v, --verbose:
      python interpreter.py -v filename
        or 
      python interpreter.py --verbose filename

    Prints the assembly code instructions as they are being executed. Useful for evaluating a program's control flow.
    Since this clutters the output, characters written to the screen are preceded by "[!] Output:"


    -a, --assemble:
      python interpreter.py -a filename
        or 
      python interpreter.py --assemble filename

    Interprets the file as assembly code instead of machinecode, and translates the assembly to machinecode using the RUN1920
    assembler ("bin/windows/assembler.exe" for Windows, "bin/linux/assembler" for Linux and "bin/macos/assembler" for MacOSX).

    For example:  python interpreter.py -a example.asm  assembles the file "example.asm" using the correct assembler for the
    user's operating system. The output file, which will be "example.hex", is then read and executed.

    If the assembly fails, the assembler's error message will be displayed.


    -m, --memory:
      python interpreter.py -m MEMORY filename
        or 
      python interpreter.py --memory MEMORY filename

    Sets the amount of memory this program will use. The size of the memory will be equal to 4 * MEMORY bytes. In other
    words, MEMORY equals the amount of 32 bit words the memory of the interpreter contains.

    Useful for very large programs, or programs that use the stack a lot, like functions with deep recursion.
    
    If the amount of memory specified is less than the amount of machinecode instructions, the memory size is increased
    in order to fit this machinecode. However, it does not leave room for the stack.

    Default value: 1024


    -sm, --show-memory:
      python interpreter.py -sm filename
        or 
      python interpreter.py --show-memory filename

    After execution of the machinecode, the RAM layout is displayed.


    -sr, --show-registers:
      python interpreter.py -sr filename
        or
      python interpreter.py --show-registers filename

    After execution of the machinecode, the registers are displayed.

    -k, --keyboard:
      python interpreter.py -k filename
        or
      python interpreter.py --keyboard filename

    Enables advanced keyboard behaviour, in which keystrokes are read to an internal buffer
    instead of reading from stdin. See also the Keyboard section below.

These flags can be used simultaneously. For example:

    python interpreter.py -m 2048 -sm example.hex  
    python interpreter.py -av example.asm


Keyboard
--------

The interpreter's standard behaviour of reading keyboard input from address `[-512]` is done by reading inputs from
`stdin`. However, this input does not register until the user has pressed the Enter key, which generally makes it hard
to read real-time input from the keyboard.

The interpreter also supports real-time user input, if the python module `getkey` is installed:

    pip install getkey

In this advanced behaviour, the interpreter keeps track of a buffer of keyboard inputs. Whenever we read from address
`[-512]` using assembly, the first value of this buffer is returned and removed from the buffer. If the buffer is empty,
the value 0 will be returned.

This advanced keyboard behaviour will be enabled if the `getkey` module is installed, and the `--keyboard` flag is
passed.