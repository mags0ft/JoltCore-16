; Simply a tiny program to test the new JC16 ISA features
; (namely shorter inline immediates and encapsulated operations)

main:
    add r1, r3, r0                 ; the most "plain" add command we can think of
    ; this should generate binary with a "dummy" encapsulated NOP operation, so
    ; we technically don't actually alter the value before using it

    add r2, r2, #5                 ; now, a standard addition with inline immediate...
    add r2, #5, r2                 ; another form, to make sure we didn't break immediates

    add r0, r0, (lshift r0, #2)    ; an add instruction with encapsulated operation
    add r1, (rshift r1, #4), r1    ; another one, just to make sure everything works
    
    sub r2, (not r3), r4           ; test whether "not" works

    halt                           ; stop the program execution

; build in all possible formats using:
; ./jcasm ./asm/programs/tiny.asm -o ./asm/build/tiny.out -dO -f bBrx