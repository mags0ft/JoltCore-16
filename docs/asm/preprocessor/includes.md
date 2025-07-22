# Includes

If you want to re-use certain areas and blocks of code, you can bundle those into files and include their definitions and thus, functionality, from anywhere.
Using this feature is really simple.

## Usage

Place an `include` statement anywhere in the code, each on its own line, to import preprocessor definitions from another file. You can use any path notation you like - which doesn't mean you should, of course.

```
include asm/libraries/math.asm              ; best option!

include ~/Documents/project/lib/div.asm     ; please avoid this
include ../../coding/jcasm/engine.asm       ; also, try to avoid this

main:
    ldi mlib_operand_a_reg!, #40
    ldi mlib_operand_b_reg!, #3

    mlib_multiply!

    halt
```

## Things to remember

Note that this statement will only import preprocessor definitions, not any actual code blocks like `main` - this behavior is intentional, as including files would otherwise always either...

- A\) require each of the included files not to have any code but only definitions - and thus not be possible to assemble as standalones, or
- B\) let the files work as standalones, too, but import potentially several `main` code blocks into the file that is including them, causing conflicts.

Thus, the design decision of only importing preprocessor definitions was made. Including a file will not include any code outside of definitons.
