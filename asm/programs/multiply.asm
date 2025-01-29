; This example program demonstrates how to multiply two arbitrary 16-bit numbers in software.
; It uses some bit-shifting trickery to achieve the result of a multiplication.
;
; All the definition's code is using the scoping capabilities of JCASM, so you can use the definition several times.

define EXAMPLE_OP_A { #6 }
define EXAMPLE_OP_B { #19 }

define operand_a_reg { ra }
define operand_b_reg { rb }
define res_reg { rc }
define dummy_reg { rd }

define multiply {
    ldi res_reg!, #0                            ; init result to zero

mul_add_scope!:
    and dummy_reg!, operand_b_reg!, #1          ; least significant bit of r1 is 1?
    jiz mul_skip_add_scope!                     ; no: skip the addition
    add res_reg!, res_reg!, operand_a_reg!      ; else: add to r2

mul_skip_add_scope!:
    lshift operand_a_reg!, operand_a_reg!, #1   ; lshift operand a by 1 (a * 2)
    rshift operand_b_reg!, operand_b_reg!, #1   ; rshift r1 by 1 (to get next LSB)
    jnz mul_add_scope!                          ; loop until done
}

main:
    ldi r0, EXAMPLE_OP_A!
    ldi r1, EXAMPLE_OP_B!

    multiply!                                   ; invoke the definition

    halt
