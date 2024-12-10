# The number of general purpose registers available on the CPU
REGISTERS_AVAILABLE = 8

# How many bits the CPU supports (for assemble-time checking)
BIT_COUNT = 16

# Highest integer the CPU can handle
MAX_INT = (2**BIT_COUNT) - 1

# maximum ROM the CPU can use
AVAILABLE_ROM = MAX_INT

# length in bits of each instruction
INSTRUCTION_LENGTH = 32
