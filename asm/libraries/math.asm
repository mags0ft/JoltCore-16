; This is a small mathematics library that can be easily extended in the future. It is intended to be included by other assembly source files.
; The goal is to provide helpful definitions that can be invoked from other scripts.

define mlib_operand_a_reg { ra }
define mlib_operand_b_reg { rb }

define mlib_res_reg { rc }
define mlib_remainder_reg { rd }

define __dummy_reg { re }

define mlib_BIT_LENGTH { #16 }

define mlib_multiply {
    ldi mlib_res_reg!, #0                                               ; init result to zero

mul_add_scope!:
    and __dummy_reg!, mlib_operand_b_reg!, #1                           ; least significant bit of r1 is 1?
    jiz mul_skip_add_scope!                                             ; no: skip the addition
    add mlib_res_reg!, mlib_res_reg!, mlib_operand_a_reg!               ; else: add to r2

mul_skip_add_scope!:
    lshift mlib_operand_a_reg!, mlib_operand_a_reg!, #1                 ; lshift operand a by 1 (a * 2)
    rshift mlib_operand_b_reg!, mlib_operand_b_reg!, #1                 ; rshift r1 by 1 (to get next LSB)
    jnz mul_add_scope!                                                  ; loop until done
}
