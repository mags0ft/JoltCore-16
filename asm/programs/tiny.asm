; Simply a tiny program to test the new JC16 ISA features
; (namely shorter inline immediates and encapsulated operations)

main:
    add r2 r2 #5                   ; starting off with a standard addition...

    add r0, r0, (lshift r0, #2)    ; an add instruction with encapsulated operation
    add r1, (rshift r1, #4), r1    ; another one, just to make sure everything works
    
    halt                           ; stop the program execution

; build in all possible formats using:
; $ ./jcasm ./asm/programs/tiny.asm -o ./asm/build/tiny.out -dO -f bBrx