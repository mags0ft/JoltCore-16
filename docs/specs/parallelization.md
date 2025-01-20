# Parallelization

The JC16 CPU is able to determine a given pair of instructions to be able to run in parallel. This significantly increases throughput, with the important drawback of it requiring twice the RAM bandwidth.

## Requirements

For any two instructions to work in parallel, these requirements need to be met by the second instruction which is tried to be executed at the same time:

- its operands do not include the target register of the first instruction
- if the instruction is using the ALU, determine if it has an encapsulated, non-NOP operation and check if said operation accesses the target register of the first instruction

The first instruction needs to meet these requirements:

- no `jmp`-like command
- no `halt`

The CPU consists of two execution cores which share their registers, program counter and ALU output flag bits.
