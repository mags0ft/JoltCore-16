from error_handling import codegen_debug_info, codegen_error
from spec import AVAILABLE_ROM, INSTRUCTION_LENGTH
from commands import Instruction, JumpInstruction


def generate_binary_from_parsed(
    parsed: "list[Instruction]", optimize: bool = False, debug_info: bool = False
):
    generated: str = ""
    instr_used: int = 0
    rom_addr_shift: int = (
        0  # by how many addresses we have to subtract if optimization was done
    )

    for el in parsed:
        # if this is a jump instruction, we need to adjust it's target address!
        if optimize and isinstance(el, JumpInstruction):
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
    {(instr_used/AVAILABLE_ROM)*100:.1f}% of ROM occupied"""
        )

    return generated


def write(bin_: str, filename: str):
    with open(filename, "w") as f:
        f.write(bin_)
