; This example program demonstrates how to multiply two arbitrary 16-bit numbers
; in software. It uses some bit-shifting trickery to achieve the result of a
; multiplication by importing the JCASM math library.

; import math library for multiplication support (no native op on JC16 exists)
include asm/libraries/math.asm

define EXAMPLE_OP_A { #6 }
define EXAMPLE_OP_B { #19 }

main:
    ; we want to perform 1024 rounds of multiplication, just for demonstration
    ; purposes
    ldi r7, #1024

loop:
    ldi mlib_operand_a_reg!, EXAMPLE_OP_A!
    ldi mlib_operand_b_reg!, EXAMPLE_OP_B!

    mlib_multiply!     ; invoke the imported definition

    sub r7, r7, #1     ; decrement loop counter
    jnz loop

finish:
    halt
