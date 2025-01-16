; A simple program that counts to 128, then halts.

define GOAL { #127 }                            ; what goal we want to hit (minus one, because we use "gt", not ">=")
define counting_reg { r0 }                      ; which register to use for counting

define __scratchpad_reg { r7 }                  ; register to use as "scratchpad"

count:
    add counting_reg! counting_reg! #1          ; increment by one
    gt __scratchpad_reg! counting_reg! GOAL!    ; check if we've hit the goal
    jiz count                                   ; if the answer is 0 (false), continue
    halt                                        ; otherwise, halt

main:
    ldi counting_reg! #0                        ; initialize the counting register to zero
    jmp count                                   ; begin the routine!
