
Interpreter for the machinecode of the RUN1718 CPU, by the Radboud University
Nijmegen. Based on assembly and machinecode by David N. Jansen.


Requirements
------------

Python 2 or 3


Usage
-----

In a Windows command prompt, or a Linux/MacOSX terminal, enter the following command:  
    python interpeter.py filename

For example:  python interpreter.py example.rom  reads the contents of the file "example.rom" as machinecode, and executes it.


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

    Interprets the file as assembly code instead of machinecode, and translates the assembly to machinecode using the
    RUN1718 assembler ("assembler.exe" for Windows, "assembler_linux" for Linux and "assembler_mac" for MacOSX).

    For example:  python interpreter.py -a example.asm  assembles the file "example.asm" using the correct assembler for the
    user's operating system. The output file, which will be "example.rom", is then read and executed.

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

These flags can be used simultaneously. For example:  
    python interpreter.py -m 2048 -sm example.rom  
    python interpreter.py -av example.asm
