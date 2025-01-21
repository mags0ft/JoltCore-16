# Comments in assembly

To comment on your code, you can simply write a semicolon `;` - anything following it will be ignored by the assembler.

## Example

```
; the entire line is a comment!

main:
    ; this is a comment inside of a label
    ldi r0, #42                 ; this is a comment beneath an instruction
    ; lshift r0, r0, #1         <-- we commented this instruction out! It won't be included.
    halt
```
