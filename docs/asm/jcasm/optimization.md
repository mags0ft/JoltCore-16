# Optimization performed by the assembler

The assembler performs some simple optimization. Besides merely **avoiding rookie mistakes and annoyances**, such as...

- replacing comments with `nop`s instead of excluding them from the build
- inserting separate instructions for jump labels instead of just jumping to the next instruction below the label

... some slightly more advanced, though experimental optimization is performed.

Currently, optimization is still very limited and experimental. Only use it if you are sure this won't critically affect your program flow, because there may still be problems.

## Redundant operation elimination

The JCASM will detect and eliminate instructions in your code that do not do anything. For example,

```
add r1, r1, #0
```

will be eliminated automatically and thus get excluded from the build due to the fact that

$$x = x + 0$$

The assembler will align all following instruction ROM addresses accordingly, so program flow stays unimpacted. However, the optimizer will inform you about the removal of such instructions as long as the [debugging flag](./flags.md) (`-d` or `--debug`) is specified.
