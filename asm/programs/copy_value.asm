; This program will attempt at copying the value of r0 into all other registers
; as quickly as possible. It's helpful to benchmark the effectiveness of the
; parallelization.

define VALUE_TO_COPY { #238 }

main:
    ; load the value to copy
    ldi r0, VALUE_TO_COPY!

    ; prevent parallelization stall, instead add the value.
    ; limitation: VALUE_TO_COPY must be no bigger than 255 (inline immediates
    ; are 8-bit)
    add r1, r1, VALUE_TO_COPY!

    ; now, copy the rest
    add r2, r0, #0
    add r3, r0, #0
    add r4, r0, #0
    add r5, r0, #0
    add r6, r0, #0
    add r7, r0, #0

    ; finish
    halt
