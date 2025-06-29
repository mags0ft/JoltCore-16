; An extremely barebones program, just to test if the parallelization feature
; works correctly. It is even more stripped-down than the
; ./asm/programs/parallelization.asm program to make it easier to understand and
; verify against the behavior of the CPU.

main:
    ; Load the values to work with
    ldi r0, #4
    ldi r1, #8
    ldi r2, #5
    ldi r3, #7

    add r0, r1, r1  ; r0 = 16
    add r2, r3, r3  ; r2 = 14
    add r1, r0, r0  ; r1 = 32
    add r3, r2, r2  ; r3 = 28

    add r0, r1, r1  ; r0 = 64
    add r2, r3, r3  ; r2 = 56
    add r1, r0, r0  ; r1 = 128
    add r3, r1, r1  ; r3 = 256

    ; We're done
    halt
