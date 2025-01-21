# Scopes

Scopes are a useful feature that go hand-in-hand with definitions. Sometimes, your definition will need to perform a jump to another label inside of itself - but because of how definitions work, there will be one central label placed and all other jumps will go to that one instead of their own ones, resulting in a loss of the original call location. Take this for example:

```
define unscoped_buggy_function {
    jmp count

count:
    sub r0, r0, #1
    jnz count
    ; otherwise, move on with the program
}

main:
    ldi r0, #40
    unscoped_buggy_function!

    ldi r0, #8
    unscoped_buggy_function!

    halt
```

This will preprocess to:

```
define unscoped_buggy_function {
    jmp count

count:
    sub r0, r0, #1
    jnz count
    ; otherwise, move on with the program
}

main:
    ldi r0, #40
    jmp count

count:
    sub r0, r0, #1
    jnz count
    ; otherwise, move on with the program

    ldi r0, #8
    jmp count

count:
    sub r0, r0, #1
    jnz count
    ; otherwise, move on with the program

    halt
```

Can you spot it? Oh no! We have the label `count` two separate times now! How should the assembler know which one is the right one to jump to? This is where labels come in.
You can limit the jump to the inside of this one specific call of the definition by using the `scope!` preprocessor directive. The fixed program would look like this:

```
define scoped_fixed_function {
    jmp count_scope!

count_scope!:
    sub r0, r0, #1
    jnz count_scope!
}

main:
    ldi r0, #22
    scoped_fixed_function!

    ldi r0, #9
    scoped_fixed_function!

    halt
```

This will be preprocessed to custom labels for each call, eliminating the problem:

```
define unscoped_buggy_function {
    jmp count

count:
    sub r0, r0, #1
    jnz count
    ; otherwise, move on with the program
}

main:
    ldi r0, #40
    jmp count_84a685bf_9978_43d4_807a_ac6d48209598

count_84a685bf_9978_43d4_807a_ac6d48209598:
    sub r0, r0, #1
    jnz count_84a685bf_9978_43d4_807a_ac6d48209598
    ; otherwise, move on with the program

    ldi r0, #8
    jmp count_4be4132e_73a9_45a2_80b5_b529db8edb71

count_4be4132e_73a9_45a2_80b5_b529db8edb71:
    sub r0, r0, #1
    jnz count_4be4132e_73a9_45a2_80b5_b529db8edb71
    ; otherwise, move on with the program

    halt
```

See? There are two separate count functions now, `count_84a685bf_9978_43d4_807a_ac6d48209598` and `count_4be4132e_73a9_45a2_80b5_b529db8edb71`. These will not interfere with each other and keep the position in the program while jumping inside of definitions.
