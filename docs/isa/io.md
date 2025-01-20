# I/O operations

The JC16 supports I/O operations to interact with devices connected to it, a.e. in the logic simulator. This is useful if you want to work with things like displays, buttons and sound.

_For the `oclk` (clock output) instruction, see the [miscellaneous instructions](./misc.md) document._

## Concept

To interact with the device(s) connected to the CPU, so-called I/O pins are used. There are 8 16-bit wide pins in total (4 for input, 4 for output) on the JC16.
These can be individually addressed by the assembly program using the value of registers. As those are no ALU operations, they do not support inline immediates yet.

## Read data from an input pin

Mnemonic: `rdpin`
Arguments:
- destination register (3 bits)
- register holding the ID of the pin to read from

Example code to read data from pin 3 to register 1:

```
define pin_id { #3 }
define reg_pin_id { r0 }
define reg_result { r1 }

main:
    ldi reg_pin_id!, pin_id!
    rdpin reg_result!, reg_pin_id!
    halt
```

## Write data to an output pin

Mnemonic: `wrpin`
Arguments:
- register holding the ID of the destination pin to write to
- register containing the value to write

Example code to write data from register 1 to pin 3:

```
define pin_id { #3 }
define reg_pin_id { r0 }
define reg_data { r1 }

main:
    ldi reg_pin_id!, pin_id!
    wrpin reg_pin_id!, reg_data!
    halt
```
