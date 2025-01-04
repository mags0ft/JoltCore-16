; Test program for the assembler to compile into binary machine instructions.
; Let's start with something simple...

main_second_part:           ; out of order code shouldn't be a problem as long as it is compiled
                            ; correctly - the main block will be the entry point
    add r2 r0 #2            ; subtract 2 from register A (0) and write into register C (2)
    sub r3 rb r0            ; subtract register 0 (A) from register b (1) and write into register 3 (D)

    halt                    ; and we're done!

jumptest:                   ; this is a new code block
    oclk                    ; do something random, just to show the block does something
    jmp main_second_part    ; back to our original program

main:                       ; main should be moved to the top by the assembler
    ldi r0 #4               ; load number 4 into register 0
    ldi rb #6               ; load number 6 into register b (register 1)

    add r0 r0 #0            ; do nothing to test optimization features
    rshift rb rb #0         ; again, just in another manner
    lshift rb rb #2         ; this should not be optimized away

    jmp jumptest            ; go to our jumptest code block
