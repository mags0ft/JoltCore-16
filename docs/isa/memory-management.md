# Memory management

To work with the up to 128 KiB of external addressable RAM, the JC16 allows you to utilize two instructions for reading from and writing to RAM.
As the ISA is designed in a way that forces every instruction to execute in exactly one clock cycle, the RAM must have an accordingly low latency.

## Read data from RAM

Mnemonic: `ldram`

Arguments:
- destination register (3 bits)
- static RAM address (can be denoted with a dollar sign for more clarity)

This instruction will load one word (2 bytes) from the according memory cell.

Example code to read data from RAM cell 0 to register 0:

```
main:
    rdram r0, $0
    halt
```

## Store data in RAM

Mnemonic: `stram`

Arguments:
- source register (3 bits)
- static RAM address to place the data in

This instruction will write one word (2 bytes) to the according memory cell.

Example code to write data to RAM cell 0 from register 0:

```
main:
    stram r0, $0
    halt
```

Support for storing and loading dynamic RAM addresses defined by register values may be added in the future; for now, RAM addresses are to be defined statically.
