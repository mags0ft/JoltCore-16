from typing import Union
from error_handling import codegen_debug_info, codegen_error
from spec import AVAILABLE_ROM, INSTRUCTION_LENGTH, OUTPUT_EXTENSIONS
from commands import Instruction, JumpInstruction


def generate_build_from_parsed(
    parsed: "list[Instruction]",
    formats: str,
    optimize: bool = False,
    debug_info: bool = False,
):
    if debug_info:
        codegen_debug_info(f'generating build for formats "{formats}"')

    generated: str = ""
    instr_used: int = 0
    rom_addr_shift: int = (
        0  # by how many addresses we have to subtract if optimization was done
    )

    for el in parsed:
        # if this is a jump instruction, we need to adjust it's target address!
        if isinstance(el, JumpInstruction):
            el.arguments[0].value -= 1

            if optimize:
                # optimizations will remove some instructions due to them doing nothing.
                # this needs to be accounted for in jump instructions, so they're
                # adjusted accordingly.

                el.arguments[0].value -= rom_addr_shift

        compiled: str = el.generate_binary(optimize, debug_info)
        did_return_something: bool = compiled.strip() != ""
        generated += compiled + ("\n" if did_return_something else "")

        if did_return_something:
            instr_used += 1
        else:
            # oh, we apparently optimized something!
            if not optimize:
                codegen_error(
                    f"unable to generate code for line {el.debug_line+1} (no \
binary was returned even though optimizations are turned off - this might be \
an internal assembler error)"
                )

            rom_addr_shift += (
                1  # our instructions will now all be up by one address in ROM!
            )

    if debug_info:
        codegen_debug_info(
            f"""compilation succeeded!
    {instr_used} instructions used ({(instr_used*INSTRUCTION_LENGTH)/1024:.2f} KiB)
    {(instr_used/AVAILABLE_ROM)*100:.1f}% of {(AVAILABLE_ROM)/1024:.1f} KiB ROM occupied"""
        )

    for format_ in formats:
        if debug_info:
            codegen_debug_info(
                f'formatting build as "{OUTPUT_EXTENSIONS[format_].upper()}"...'
            )
        if format_ == "x":
            # hexadecimal output
            finalized: str = ""

            for line in blockify(generated).splitlines():
                finalized += f"{int(line.replace(' ', ''), 2):x} "

            yield (finalized.strip(), OUTPUT_EXTENSIONS[format_], False)
        elif format_ == "b":
            # standard formatted binary
            yield (generated, OUTPUT_EXTENSIONS[format_], False)
        elif format_ == "B":
            # block binary format (no spaces, all lines have the same length)
            yield (blockify(generated), OUTPUT_EXTENSIONS[format_], False)
        elif format_ == "r":
            # raw binary ROM file

            res = b""
            # raw_instr = [int(i, 2) for i in ]

            for instr in blockify(generated).splitlines():
                res += int(instr, 2).to_bytes(4, "big")

            yield (res, OUTPUT_EXTENSIONS[format_], True)
        elif format_ == "p":
            pass
        else:
            codegen_error(f'unknown output format "{format_}"')


def blockify(generated):
    finalized: str = ""

    for line in generated.splitlines():
        processed = line.replace(" ", "")
        finalized += processed + ("0" * (INSTRUCTION_LENGTH - len(processed))) + "\n"

    return finalized.strip()


def write(bin_: "Union[str, bytes]", filename: str, binary: bool = False):
    with open(filename, ("wb" if binary else "w")) as f:
        f.write(bin_)
