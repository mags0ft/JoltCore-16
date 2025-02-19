# The number of general purpose registers available on the CPU
REGISTERS_AVAILABLE = 8

# How many bits the CPU supports (for assemble-time checking)
BIT_COUNT = 16

# How many bits the inline immediate parameters can have in various scenarios
INLINE_IMMEDIATE_BIT_COUNT = 8
ENCAPSULATED_INSTRUCTION_INLINE_IMMEDIATE_BIT_LENGTH = 3

# What the maximum values for these parameters are due to their bit count
MAX_INLINE_IMMEDIATE = (2**INLINE_IMMEDIATE_BIT_COUNT) - 1
MAX_ENCAPSULATED_INSTRUCTION_INLINE_IMMEDIATE = (
    2**ENCAPSULATED_INSTRUCTION_INLINE_IMMEDIATE_BIT_LENGTH
) - 1

# Highest integer the CPU can handle
MAX_INT = (2**BIT_COUNT) - 1

# length in bits of each instruction
INSTRUCTION_LENGTH = 24

# maximum ROM the CPU can use
AVAILABLE_ROM = MAX_INT * (INSTRUCTION_LENGTH // 8)

OUTPUT_EXTENSIONS = {"b": "bin", "B": "bbin", "x": "hex", "r": "rom", "p": "asm"}
