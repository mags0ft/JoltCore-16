; register for counting
000 ldi 0 0

; register for adding
001 ldi 1 1

; registers for pin descriptions
; position pin
002 ldi 2 0

; color red pin
003 ldi 3 1

; color green pin
004 ldi 4 2

; color blue pin
005 ldi 5 3

; set greater than register to zero
006 ldi 6 0

; set maximum value of counter
007 ldi 7 512

; write current counter reg to pin red by selecting pos and color
008 wrpin 0 2
009 wrpin 0 3
010 oclk

; increase counter
011 add 0 0 1

; check if program done
012 gt 6 0 7
013 jiz 8

; halt if it is
014 halt
