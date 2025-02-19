; This program will attempt to print "Hello world" to a connected Logisim
; terminal.

include asm/libraries/screen.asm

main:
    ; describe where our pins are located
    ldi srclib_screen_char_port!, #0

    ; now, it's time for some glorious assembly spaghetti code!
    ; (there is no string type or array to loop over implemented in jcasm yet)
    ldi scrlib_char!, #H
    scrlib_write_to_screen!
    ldi scrlib_char!, #e
    scrlib_write_to_screen!
    ldi scrlib_char!, #l
    scrlib_write_to_screen!
    ldi scrlib_char!, #l
    scrlib_write_to_screen!
    ldi scrlib_char!, #o
    scrlib_write_to_screen!
    ldi scrlib_char!, #32   ; (space)
    scrlib_write_to_screen!
    ldi scrlib_char!, #w
    scrlib_write_to_screen!
    ldi scrlib_char!, #o
    scrlib_write_to_screen!
    ldi scrlib_char!, #r
    scrlib_write_to_screen!
    ldi scrlib_char!, #l
    scrlib_write_to_screen!
    ldi scrlib_char!, #d
    scrlib_write_to_screen!

    halt
