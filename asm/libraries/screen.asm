; Tiny library to talk to the Logisim terminal screen.

define scrlib_char { r4 }
define srclib_screen_char_port { r5 }

define scrlib_write_to_screen {
    ; Definition to write a character inside scrlib_char to the terminal
    ; by invoking a clock signal on the port inside scrlib_screen_clk_port.
    ; This will not alter the values of any input registers.

    wrpin scrlib_char!, srclib_screen_char_port!
    oclk
}

define scrlib_clear_pixel {
    ; Definition to clear a pixel on the screen.
    ; Invokes scrlib_write_to_screen at assembly time. Uses r4 and r5.

    ldi scrlib_char!, #0
    scrlib_write_to_screen!
}
