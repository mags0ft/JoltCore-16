# Definitions

To label certain registers or reduce overall writing effort, you can use so-called definitions.

## Usage

Write a `define` statement anywhere in your assembly source file, followed by an identifier (stick to the [naming scheme](../syntax.md)) and the body enclosed in curly braces.
You can then use said defined value by writing its name out, followed by an exclamation mark: `!`

An example:

```
define counting_register { r0 }
define step_size { #1 }

main:
    ldi counting_register!, #16
    jmp countdown

countdown:
    sub counting_register!, counting_register!, step_size!
    jnz countdown
    halt
```

## More complex routines

You can also use definition to create a primitive type of macro, taking register contents as "arguments" - because there is no problem with definitions taking up multiple lines:

```
define complex_calculation {
    add r0, r0, (lshift r1, #1)
    sub r0, #2
    not r0, r0
}

main:
    ldi r0, #32
    ldi r1, #4
    complex_calculation!

    ldi r0, #16
    ldi r1, #2
    complex_calculation!

    halt
```

Of course, if such definition performs any jumps, this will jump to one central location independent from the call location (as this doesn't implement a stack) and won't be scoped to that single use. To achieve this, use [scopes](./scopes.md).
