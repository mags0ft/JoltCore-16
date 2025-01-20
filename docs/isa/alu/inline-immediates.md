# Inline immediates

All ALU instructions support the use of inline immediates which can save from you an abundance of extra `ldi` calls.

Unlike the separate `ldi` instruction, the inline immediates only support up to 8-bit numbers due to lack of space - after all, we only have 24 bits per instruction to work with and the ALU operation itself needs a fair share of that.

Inside of encapsulated ALU operations, space is even more limited, allowing values from 0 to 7 (3-bit long inline immediate). These may be called "tiny immediates".

## Usage

Simply denote an immediate by writing a hashtag in front of it. Be aware that you can only use one immediate per instruction due to, again, space constraints.

Example:

```
main:
    add r0, r0, #3      ; add 3 to the value of register 0, then write back
    halt
```
