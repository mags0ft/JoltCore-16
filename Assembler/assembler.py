#!/bin/bash

"""
This is the assembler for the JCS16 written in Python.
"""

import os
import sys
from colorama import Fore

from instruction_set import (
    INSTRUCTIONS,
    REGISTERS_AVAILABLE,
    ALU_INSTRUCTIONS,
    JUMP_INSTRUCTIONS,
    MAX_INT,
    AVAILABLE_ROM,
    BIT_COUNT
)


# the input file to process
input_file: str = sys.argv[1]


def asm_error(e: str, line: str):
    """
    Throw errors while assembling
    """

    print(
        f'''
{Fore.RED}error assembling \"{input_file}\"{Fore.RESET}:
    {line}
    {Fore.YELLOW}{e}{Fore.RESET}
    '''
    )

    sys.exit(-1)


def check_register(reg, line):
    """
    Check if a register does exist
    """
    
    if reg > REGISTERS_AVAILABLE:
        asm_error(
            f"Too high register {reg_dest}, max is {REGISTERS_AVAILABLE}.",
            line
        )


def check_int(int_, line):
    """
    Check if an integer is too high to be supported by the CPU
    """

    if int_ > MAX_INT:
        asm_error(f"Too high integer {int_}, max is {MAX_INT}.", line)


with open(input_file, "r") as f:
    lines: list[str] = [i.strip().split(";")[0] for i in f.readlines()]


# filter for comments and remove empty lines
lines = list(filter(
    lambda l: l and (
        not (" ".join(l.split()[1:])).startswith(";")
    ), lines
))
assembled: list[str] = []


for line in [(" ".join(i.split()[1:])) for i in lines]:
    if not line:
        # skip lines that somehow got stripped empty
        # (cannot happen as of now due to the filter above, however
        # is kept for future extensions to catch potential bugs)
        continue

    translated: str = ""
    split_line = line.split()

    command: str = split_line[0]

    try:
        translated += INSTRUCTIONS[command] + " "
    except KeyError:
        asm_error(f"Unknown instruction code \"{command}\".", line)


    if command in ALU_INSTRUCTIONS:
        reg_dest: str = int(split_line[1])
        reg_src1: str = int(split_line[2])
        reg_src2: str = int(split_line[3]) if command != "not" else 0

        check_register(reg_dest, line)
        check_register(reg_src1, line)
        if command != "not":
            # not instructions do not require reg B
            check_register(reg_src2, line)

        translated += bin(reg_dest)[2:].zfill(3) + " "
        translated += bin(reg_src1)[2:].zfill(3)
        translated += bin(reg_src2)[2:].zfill(3)

        translated += "0" * 10 # there aren't any more args needed

    elif command in JUMP_INSTRUCTIONS:
        translated += "000 " # reg_dest is nulled in jmp-like instructions
        translated += bin(int(split_line[1]))[2:].zfill(BIT_COUNT)

    elif command == "ldi":
        reg_dest: str = int(split_line[1])
        value: str = int(split_line[2])

        check_register(reg_dest, line)
        check_int(value, line)

        translated += bin(reg_dest)[2:].zfill(3) + " "
        translated += bin(value)[2:].zfill(BIT_COUNT)

    elif command in ["halt", "oclk"]:
        translated += "000" + " " + "0" * BIT_COUNT

    elif command in ["wrpin", "rdpin"]:
        reg_dest: str = int(split_line[1])
        reg_src1: str = int(split_line[2])

        check_register(reg_dest, line)
        check_register(reg_src1, line)

        translated += bin(reg_dest)[2:].zfill(3) + " "
        translated += bin(reg_src1)[2:].zfill(3)

        translated += "0" * 13 # there aren't any more args to give


    # after generating assembled instruction, add it to the buffer
    assembled.append(translated)


output_filename_base = os.path.join(
    ".",
    "build",
    (input_file.split("/")[-1].split("\\")[-1])
)


# write the binary file with zeroes and ones in form of a
# "human-readable" string to allow pasting in other editors
with open(output_filename_base + ".bin", "w") as f:
    f.write("\n".join([i for i in assembled]))


# write the same file in hex format to allow pasting in Logisim
with open(output_filename_base + ".hex", "w") as f:
    out = []
    for i in [i.replace(" ", "") for i in assembled]:
        out.append(hex(int(i, 2))[2:])
    f.write("\n".join(out))


# finish
print(f'''
{Fore.GREEN}Assembled \"{input_file}\" successfully{Fore.RESET}
    Program is using {len(assembled)} / {AVAILABLE_ROM} instructions ({(len(assembled) / AVAILABLE_ROM) * 100:.2f}% ROM)
''')
