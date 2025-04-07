# JCEMU

JCEMU (JoltCore Emulator) is the fast and easy-to-use emulator for the JC16v2 CPU.

## Building JCEMU locally

To get started using JCEMU, you need to compile it. There is a script provided to do so. It works on Unix-like systems.

```bash
$ chmod +x ./emu/build_jecmu && ./emu/build_jcemu
```

## Running an app in JCEMU

The JC16v2 emulator only supports running compiled assembly programs formatted in raw binary ROM format (see the [corresponding documentation](../asm/jcasm/formats.md) on how to use those in JCASM).

```bash
$ ./jcemu ./asm/build/multiply.rom
```

## Example program output

```
$ ./jcemu ./asm/build/multiply.rom 
jcemu: version v0.0.1
jcemu: halt instruction invoked
jcemu: program execution terminated, took 1058 clock cycle(s) and 0.017783ms (avg clock speed 59.5 MHz)
```
