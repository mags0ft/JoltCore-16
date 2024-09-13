"""
This module contains all the instructions translated into binary,
instruction and register names, constants and more misc variables.
"""

# All instructions usable by the CPU in binary as strings
INSTRUCTIONS = {
    "add":      "00000",
    "sub":      "00001",
    "and":      "00010",
    "not":      "00011",
    "or":       "00100",
    "xor":      "00101",
    "nand":     "00110",
    "nor":      "00111",
    "lshift":   "01000",
    "rshift":   "01001",
    "gt":       "01010",
    "lt":       "01011",
    "eq":       "01100",

    "jmp":      "10000",
    "jiz":      "10001",
    "jnz":      "10010",
    "jic":      "10011",
    "jnc":      "10100",

    "oclk":     "10111",
    "ldi":      "11000",
    "ldram":    "11001",
    "stram":    "11010",
    "rdpin":    "11011",
    "wrpin":    "11100",
    
    "halt":     "11111"
}


# The number of general purpose registers available on the CPU
REGISTERS_AVAILABLE = 8


# All ALU-like instructions
ALU_INSTRUCTIONS = [
    "add",
    "sub",
    "and",
    "not",
    "or",
    "xor",
    "nand",
    "nor",
    "lshift",
    "rshift",
    "gt",
    "lt",
    "eq"
]


# All Jump-like instructions
JUMP_INSTRUCTIONS = [
    "jmp",
    "jiz",
    "jnz",
    "jic",
    "jnc"
]


# How many bits the CPU supports (for assemble-time checking)
BIT_COUNT = 16


# Highest integer the CPU can handle
MAX_INT = (2 ** BIT_COUNT) - 1


# maximum ROM the CPU can use
AVAILABLE_ROM = MAX_INT
