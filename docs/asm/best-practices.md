# Best practices

To write good and performant assembly, these are a few best practices to keep in mind.

## Be aware of the entire ISA

The JC16 ISA doesn't only have instructions like `jiz` (jump if zero) but also `jnz` (jump if non-zero). This helps save a few clock cycles every now and then.

Instead of this:

```
main:
    ldi r0, #30
    jmp count

count:
    sub r0, r0, #1
    jiz finish
    jmp count

finish:
    halt
```

Write this:

```
main:
    ldi r0, #30
    jmp count

count:
    sub r0, r0, #1
    jnz count
    halt
```

Indeed, if you want to sacrifice a little bit of readability, you can also leave the first entry-point jump instruction out because the program counter will increment right into the next label if the last one does not end with a jump-like instruction. Be aware that this is dangerous though, as the assembler re-orders the labels to move `main` to the top (all others are kept in order). Know what you are doing!

Fully optimized version:

```
main:
    ldi r0, #30

count:
    sub r0, r0, #1
    jnz count
    halt
```

## Optimize maths where applicable

If you want to multiply or divide by a power of two, use bit shift operations:

```
main:
    ldi r0, #4
    lshift r0, r0, #2       ; multiply by 4
    rshift r0, r0, #1       ; divide by 2
```

The amount of bits you shift correspond to the number you are multiplying/dividing with; shifting by one means 2, shifting by 2 means 4, shifting by 3 means 8 etc.

## Keep the naming schemes in mind

Read the docs on [naming labels and definitions here](./syntax.md).

## Comment your code

To make the already-hard-to-grasp assembly a bit easier for others to read, please consider [commenting](./comments.md) your code properly!
