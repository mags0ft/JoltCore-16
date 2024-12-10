from error_handling import codegen_debug_info
from spec import AVAILABLE_ROM, INSTRUCTION_LENGTH
from commands import Instruction


def generate_binary_from_parsed(
    parsed: "list[Instruction]", optimize: bool = False, debug_info: bool = False
):
    generated = ""
    instr_used = 0

    for el in parsed:
        compiled: str = el.generate_binary(optimize, debug_info) + "\n"
        generated += compiled

        if compiled.strip():
            instr_used += 1

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
