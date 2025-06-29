; A simple program that counts to 128, then halts.

define GOAL { #128 }                         ; what goal we want to hit
                                             ; (-1, because we don't use ">=")
define counting_reg { r0 }                   ; which reg to use for counting

define __scratchpad_reg { r7 }               ; register to use as "scratchpad"

count:
    add counting_reg! counting_reg! #1       ; increment by one
    gt __scratchpad_reg! counting_reg! GOAL! ; check if we've hit the goal
    jiz count                                ; if the answer is no, continue
    halt                                     ; otherwise, halt

main:
    ldi counting_reg! #0                     ; initialize counting register to 0
    jmp count                                ; begin the routine!
