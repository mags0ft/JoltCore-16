define bit_ptr_reg { rd }
define bit_mask_reg { re }
define is_match_reg { rf }

define multiply {
    ldi bit_mask_reg!, #1
    ldi bit_ptr_reg!, #0
    ldi rc, #0

mul_mv_bit_ptr_scope!:
    gt is_match_reg!, bit_ptr_reg!, #16
    jnz mul_finish_scope!
    and is_match_reg!, rb, (lshift bit_mask_reg!, bit_ptr_reg!)
    add bit_ptr_reg!, bit_ptr_reg!, #1
    jiz mul_mv_bit_ptr_scope!
    add rc, rc, (lshift ra, bit_ptr_reg!)

mul_finish_scope!:
    nop rc, rc, rc
}

main:
    ldi ra, #9
    ldi rb, #7
    multiply!
    halt
