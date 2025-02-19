# Instruction syntax

The instruction syntax in JC16 assembly is rather simplistic and you should be able to get started quite easily.

## Basic syntax

In the JC16 assembly language, you generally write instructions out like this:

```
label_name:
    opcode target_register, operand_a, operand_b
```

In general, you write out one instruction per line without any semicolons for separation. You can optionally separate arguments such as operands inside of instructions using one or several commas. This is not strictly necessary though, just a bit more readable.

## Labels

To make jumping a little easier, you can create labels to jump to in your code:

```
main:
    ldi r0, #3
    ldi r1, #5
    jmp addition

addition:
    add r2, r0, r1
    jmp finish

finish:
    oclk
    halt
```

The order of those does not matter and you can put the `main` label wherever you want - it will always be moved up by the assembler and thus become the entry point.

## Immediates, registers and addresses

Immediates are denoted by a hashtag in front of them - you can also use chars inside assembly source code which will be converted to their respective ASCII codepoint upon assembly:

```
main:
    add r0, r0, #4      ; load immediate 4 ...
    add r0, r0, #A      ; ... or try chars - this is number 65!
    halt
```

(To denote special characters like spaces, you can still use the integer notation - for example, a space in ASCII is number 32, which allows you to use it by simply loading the immediate `#32` into a register!)

Registers are denoted by an `r` in front of them and can either be written using numbers from 0 to 7 or alphabetic letters from a to h:

```
main:
    add r0, r1, r2      ; registers with numbers as identifiers ...
    sub ra, rb, rc      ; ... or with letters!
    halt
```

(`r0` = `ra`, `r1` = `rb`, `r2` = `rc` etc.)

Static addresses, while not recommended to be used in jumps (because the favorable labels exist!) but instead in memory management commands, can be denoted with a dollar sign in front of them:

```
main:
    ldi r0, #1234
    stram r0, $0        ; store value of r0 at RAM address 0
    halt
```

## Identifier naming schemes

Whether it's for definitions or labels, you should stick to the identifier naming scheme:

- only numbers, alphabetic letters and underscores
- preferably `snake_case`
- not beginning with a number

Examples that work:

```
test_procedure
banana_counter
check_4x4_board
chess960
__secret_label
```

Examples that work, but should be avoided:

```
ILoveJavaSoMuchSingletonFactoryException
cool__name__yeah
Hello_world
```

Examples that do not work:

```
!"§()haha::-
#coolStuff-
function-name
print_burrito_🌯
```
