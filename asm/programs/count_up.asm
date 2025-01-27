; This program counts all registers up by 1 for 16 times to test out the parallelization

main:
    ; initialize all registers
    ldi r0, #0
    ldi r1, #0
    ldi r2, #0
    ldi r3, #0

    ldi r4, #0
    ldi r5, #0
    ldi r6, #0
    ldi r7, #0

loop:
    gt r7, r6, #16      ; is r7 bigger than 16?
    jnz finish          ; if yes, halt

    ; increase all registers by one
    add r0, r0, #1
    add r1, r1, #1
    add r2, r2, #1
    add r3, r3, #1

    add r4, r4, #1
    add r5, r5, #1
    add r6, r6, #1
    add r7, r7, #1

    jmp loop            ; run again

finish:
    ; stop execution
    halt
