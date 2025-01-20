# Miscellaneous instructions

There are a few operations that do not fit into the other categories all too well - thus, they are compiled here.

## oclk

Emits a clock signal on the clock pin. This pin is separate from the I/O system pins, which is why the documentation for this command is separate.

- Mnemonic: `oclk`
- Arguments:
    - none, fill with zeroes (JCASM does this automatically)

Example:

```
main:
    oclk
    halt
```

## halt

Stops the clock and ends program execution permanently. The clock has to be restarted manually from an outside source once this command is executed.

- Mnemonic: `halt`
- Arguments:
    - none, fill with zeroes

Example:

```
main:
    halt    ; this is the most useless program one could write
```

## nop

Technically, this is executed in the ALU. It will not perform any operation to the input value(s) at all. However, it still supports encapsulated operations which themselves are capable of doing something. You can use this command to move data around and modify it in the same time.

Specifically, it will take operand A, write it into the target register and discard operand B.

- Mnemonic: `nop`
- Arguments:
    - target register (3 bits)
    - operand A - written into the target register (3 bits)
    - operand B - discarded (3 bits)
    - encapsulated operation/inline immediate flag (2 bits)
    - instruction body (8 bits)
        - either: encapsulated operation
            - opcode (4 bits)
            - second source register or tiny inline immediate (3 bits)
            - immediate flag (1 bit)
        - or: arbitrary 8-bit immediate

All these examples are valid `nop`s:

```
main:
    nop r0, r0, r0
    nop r0, (add r1, #3), r2
    nop r0 #1 r0
```
