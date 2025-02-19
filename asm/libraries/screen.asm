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
