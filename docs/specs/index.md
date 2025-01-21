# Technical specifications

These pages contain the technical specification of the JC16 CPU with detailed information on its internals.

## Table of contents

- [Parallelization](./parallelization.md)

## General information

- Harvard load-store RISC architecture with up to 32 different instructions
- Registers:
    - 8x 16-bit general purpose
    - separate 16-bit program counter
- Busses:
    - RAM:
        - 16-bit address bus
        - 16-bit data bus
    - ROM (program memory):
        - 16-bit address bus
        - 24-bit program bus
- RAM:
    - 65536 addressable cells (16-bit each)
    - 128 KiB in total
- ROM:
    - 65536 addressable cells (24-bit each)
    - 192 KiB in total
- Instructions:
    - [JC16 custom ISA](../isa/index.md)
    - every instruction runs within one clock cycle
    - instruction execution is [parallelized](../specs/parallelization.md) when possible
    - 5-bit opcode
    - 3-bit register ID length (for addressing 8 registers in total)
    - the target register always follows the opcode
- ALU features:
    - 4-bit function code
    - bitwise logic
    - rudimentary math operations that can be done efficiently within one clock cycle
    - comparisons
