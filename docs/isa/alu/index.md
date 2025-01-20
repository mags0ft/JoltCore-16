# ALU-specific instruction set architecture

The ALU instructions are certainly one of the most important ones - they are the integral part to all calculations done by the JC16 CPU.

## Table of contents

- [Inline immediates](./inline-immediates.md)
- [Encapsulated operations](./encapsulated-operations.md)

## An overview of all operations

ALU instructions follow a specific format:

- opcode (5 bits, in ALU instructions, the first one is always `0`)
- target register (3 bits)
- operand A (3 bits)
- operand B (3 bits)
- encapsulated operation/inline immediate flag (2 bits)
- instruction body (8 bits)
    - either: [encapsulated operation](./encapsulated-operations.md)
        - opcode (4 bits)
        - second source register or ["tiny" inline immediate](./inline-immediates.md) (3 bits)
        - immediate flag (1 bit)
    - or: arbitrary 8-bit [immediate](./inline-immediates.md)

The only exception to this is the bitwise `not` operation and `nop` - these ignore the second operand B.

Available operations are:

- `add`: add two integers
- `sub`: subtract two integers
- `and`: bitwise AND
- `not`: bitwise NOT (operand B is ignored)
- `or`: bitwise OR
- `xor`: bitwise XOR
- `nand`: bitwise NAND
- `nor`: bitwise NOR
- `lshift`: left-shift operand A by operand B
- `rshift`: right-shift operand A by operand B
- `gt`: check if operand A is greater than operand B - returns `0b1` is true, `0b0` if false.
- `lt`: check if operand B is less than operand B - returns the same scheme as `gt`
- `eq`: check if the operands are equal - returns the same scheme as `gt`
- `nop`: do nothing to the operands and write back operand A into the target register (operand B is ignored)

## Usage

Examples for ALU operations:

```
main:
    add r0, r0, #1
    sub r2, r1, r0
    lshift r3, r4, (gt r0 #9)
    not r6, r6
    nop r0, r0, r0
    halt
```
