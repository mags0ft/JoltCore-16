; This program will calculate n Fibonacci numbers.

; Enter how many numbers you want to generate:
define FIB_NUMBERS_TO_CALCULATE { #24 }

; These are the registers we can use. The new assembler supports a primitive kind
; of preprocessor directives, so we can use named registers to make things simpler.
define cur_fib_num_reg { r0 }           ; register holding the current number
define prev_num_1_reg { r1 }            ; register holding the number before
define prev_num_2_reg { r2 }            ; register holding the number before before
define numbers_calculated_reg { r3 }    ; register keeping track of the progress

init:
    ldi cur_fib_num_reg!, #0
    ldi prev_num_1_reg!, #1
    ldi prev_num_2_reg!, #1
    ldi numbers_calculated_reg!, #0

    jmp calc_next_fibonacci_number

calc_next_fibonacci_number:
    add prev_num_2_reg!, prev_num_1_reg!, #0    ; move the last number into the register
                                                ; for the second-last number
    add prev_num_1_reg!, cur_fib_num_reg!, #0   ; same for the current number, which is
                                                ; is moved into the register for the
                                                ; last number

    ; all preparations are done, calculate the actual fibonacci number now:                                        
    add cur_fib_num_reg!, prev_num_1_reg!, prev_num_2_reg!

    ; increase numbers calulcated by one
    add numbers_calculated_reg! numbers_calculated_reg! #1

    ; now we can continue the cycle
    jmp check_if_done

check_if_done:
    ; check if we have reached our goal
    eq r4, numbers_calculated_reg!, FIB_NUMBERS_TO_CALCULATE!

    ; if the result is zero (false), we calculate the next number
    jiz calc_next_fibonacci_number

    ; otherwise, halt the program
    halt

main:
    ; begin the initialization sequence
    jmp init
