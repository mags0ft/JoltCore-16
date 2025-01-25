; This program has been made to test the parallelization feature on the CPU.
; Instructions inside of the "parallel" block should be executed twice as fast (PC advances by 2).
; Instructions inside of the "standard" block shouldn't do this in any case.

main:
    ; load in some arbitrary values...
    ldi r0, #8
    ldi r1, #12
    ldi r2, #19
    ldi r3, #24

    ; begin the "parallel" block, which should allow for fast execution because it can run each pair of operations in parallel
    jmp parallel

parallel:
    ; some random operations:
    add r4, r1, r2
    sub r3, r4, r0
    nor r2, r1, (lshift r0, r4)
    xor r1, (not r3), r5

    ; and almost the same stuff again, so we can see it better when it's in action:
    add r4, r3, r2
    sub r3, r4, r0
    nor r2, r1, (lshift r0, r4)
    xor r1, (not r3), r5

    ; done, now let's try some "unparallelizable" (that's certainly not a real word!) code
    jmp standard

standard:
    ; some code that depends on each previous line's result:
    sub r1, r2, #4
    add r2, #2, r1
    lshift r0, (not r2), #3
    xor r2, r4, r0

    ; and once again, so we can observe it better:
    sub r1, r2, #4
    add r2, #2, r1
    lshift r0, (not r2), #3
    xor r3, r4, r0

    halt
