# Jump instructions

In order to jump around in code, be it conditionally or not, the JC16 ISA supplies 5 jump-like instructions. All of them are listed below.
Note that apart from the plain `jmp`, the others make use of the current state of the ALU result flag bits. Thus, the lastmost ALU instruction executed before a conditional jump occurs influences if the jump is actually performed.

## Usage

There are 5 different jump-like instructions, 4 of them are conditional.

### jmp

- Mnemonic: `jmp`
- Description: Immediately jumps to the given address without any checks performed.
- Unconditional, always jumps
- Arguments:
    - no register, three bits are left out (`000`, note that JCASM will do this for you)
    - address or label to jump to (addresses can, just like in the memory instructions, be denoted with a dollar sign in front of them for more clarity)

Example:

```
main:
    jmp oclk_and_finalize

finish:
    halt

oclk_and_finalize:
    oclk
    jmp finish
```

### jiz

- Mnemonic: `jiz`
- Description: Jumps if the last ALU operation resulted in a zero (zero flag bit is set to 1)
- Conditional
- Arguments:
    - no register, three bits are left out
    - address or label to jump to

Example:

```
main:
    ldi r0, #16
    jmp countdown

countdown:
    sub r0, r0, #1
    jiz finish
    jmp countdown

finish:
    halt
```

### jnz

- Mnemonic: `jnz`
- Description: Jumps if the last ALU operation resulted in a non-zero value (zero flag bit is set to 0)
- Conditional
- Arguments:
    - no register, three bits are left out
    - address or label to jump to

Example:

```
main:
    ldi r0, #16
    jmp countdown

countdown:
    sub r0, r0, #1
    jnz countdown
    halt
```

### jic

- Mnemonic: `jic`
- Description: Jumps if the last ALU operation resulted in a carry or borrow (carry/borrow flag bit is set to 1)
- Conditional
- Arguments:
    - no register, three bits are left out
    - address or label to jump to

Example:

```
main:
    ldi r0, #65530
    jmp count_until_overflow

count_until_overflow:
    add r0, r0, #1
    jic finish
    jmp count_until_overflow

finish:
    halt
```

### jnc

- Mnemonic: `jnc`
- Description: Jumps if the last ALU operation did not result in a carry or borrow (carry/borrow flag bit is set to 0)
- Conditional
- Arguments:
    - no register, three bits are left out
    - address or label to jump to

Example:

```
main:
    ldi r0, #65530
    jmp count_until_overflow

count_until_overflow:
    add r0, r0, #1
    jnc count_until_overflow
    halt
```
