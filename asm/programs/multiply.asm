; This example program demonstrates how to multiply two arbitrary 16-bit numbers in software.
; It uses some bit-shifting trickery to achieve the result of a multiplication.
;
; All the definition's code is using the scoping capabilities of JCASM, so you can use the definition several times.

define bit_ptr_reg { rd }   ; register containing the pointer to the current bit we're iterating over
define bit_mask_reg { re }  ; register holding our current bitmask to be applied to the second operand
define is_match_reg { rf }  ; "throwaway" scratchpad register containing the value of comparative ALU operations

define multiply {
    ; We define our routine...

    ldi bit_mask_reg!, #1   ; our bitmask starts at 0b0000000000000001
    ldi bit_ptr_reg!, #0    ; our pointer begins at the first bit in operand B
    ldi rc, #0              ; the result register (a * b = c) is initialized to zero

mul_mv_bit_ptr_scope!:
    ; this codeblock will:
    ; - move the bit in the mask one to the left
    ; - check the mask against operand B
    ; - add the operand A shifted by the pointer register's value if the previous check succeeded
    ; - repeat until the final bit has been reached (16th bit as the JC16 is 16-bit)
    
    gt is_match_reg!, bit_ptr_reg!, #16                         ; are we done yet?
    jnz mul_finish_scope!                                       ; yes: jump to finish
    and is_match_reg!, rb, (lshift bit_mask_reg!, bit_ptr_reg!) ; no: check bit in operand
    jiz mul_mv_bit_ptr_scope!                                   ; if bit = 0: continue with next one
    add bit_ptr_reg!, bit_ptr_reg!, #1                          ; otherwise: increase the bit pointer
    add rc, rc, (lshift ra, bit_ptr_reg!)                       ; then, add shifted operand A to result value

mul_finish_scope!:
}

main:
    ; Let's try it out! Multiply 9 * 7:
    ldi ra, #9 
    ldi rb, #7
    multiply!

    ; The result should now be inside rc (register #2, counting up from zero)
    halt    ; finish
