; This program demonstrates how the scope system works, so you can have more elaborate definitions with jumps in them.

define countdown {
countdown_scope!:
    sub r0 r0 #1
    jnz countdown_scope!
    ; we have counted to zero! Give an output via OCLK
    oclk
}

main:
    ldi r0 #16                  ; count down from 16 to zero
    countdown!

    ldi r0 #32                  ; and now from 32 to zero
    countdown!

halt