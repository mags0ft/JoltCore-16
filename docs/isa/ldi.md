# "Load Immediate" instruction (LDI)

The LDI command is a helpful instruction to load any arbitrary 16-bit value into a register instantaneously.

## Usage

Mnemonic: `ldi`
Arguments:
- destination register (3 bits)
- 16-bit immediate

Example code to load number 54321 into register 0:

```
main:
    ldi r0, #54321
    halt
```
