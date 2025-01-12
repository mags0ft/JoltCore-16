from dataclasses import dataclass
import os
from string import ascii_lowercase

from spec import INLINE_IMMEDIATE_BIT_COUNT, MAX_INLINE_IMMEDIATE, REGISTERS_AVAILABLE
from commands import COMMANDS, Argument, Instruction
from error_handling import parse_error


@dataclass
class LineOfCode:
    # represents a line of original source code.

    content: str = ""
    original_line: int = 0

    # of which code block this line is part
    part_of: str = ""

    rom_addr: int = -1


def build_instructions(
    input_file: str, optimize: bool = False, debug_info: bool = False
):
    if not os.path.isfile(input_file):
        parse_error(f'cannot open file "{input_file}".')

    with open(input_file, "r") as f:
        content = f.read()

    return parse_file(content, optimize, debug_info)


def preprocess(s: str) -> "list[LineOfCode]":
    # does some preprocessing, most notably moves the main function up.

    res: "list[LineOfCode]" = []

    main_fn: "list[LineOfCode]" = []
    cur_in = ""

    for line_number, line in enumerate(s.splitlines()):
        stripped_line: str = line.strip()
        if stripped_line.startswith(";") or not stripped_line:
            continue

        comment_pos = line.find(";")
        processed_line = (
            line[: (comment_pos if comment_pos != -1 else len(line))]
            .strip()
            .replace(",", " ")
        )

        if (not processed_line.endswith(":")) and (not cur_in):
            parse_error("code outside of named block", {"line": line_number + 1})

        if processed_line.endswith(":"):
            cur_in = processed_line[:-1]

        loc = LineOfCode(processed_line, line_number, cur_in, -1)

        if cur_in == "main":
            main_fn.append(loc)
        else:
            res.append(loc)

    if not main_fn:
        parse_error("file does not have a main code block")

    if all([instr.content != "halt" for instr in main_fn + res]):
        parse_error("the program never halts")

    res = main_fn + res  # move the main block up!

    return res


def parse_file(
    s: str, optimize: bool = False, debug_info: bool = False
) -> "list[Instruction]":
    res = []

    lines: "list[LineOfCode]" = preprocess(s)

    # keeps track of the instruction IDs for the respective block names
    block_names = {}

    # first pass: add the ROM addresses to each line
    cur_rom_addr: int = 0
    cur_block: str = ""

    for line in lines:
        if line.content.endswith(":"):
            cur_block = line.content[:-1]
            continue

        line.rom_addr = cur_rom_addr
        cur_rom_addr += 1

        if cur_block:
            block_names[cur_block] = cur_rom_addr

        cur_block = ""

    # second pass: parse the lines
    for line in lines:
        if line.content.endswith(":"):
            continue

        res.append(parse_line(line, block_names))

    return res


def parse_line(l: LineOfCode, block_names: "dict[str, int]") -> Instruction:
    split_content: "list[str]" = l.content.split()

    opcode: str = split_content[0]
    if opcode not in COMMANDS:
        parse_error("unknown command", {"command": opcode, "line": l.original_line + 1})

    instr: Instruction = COMMANDS[opcode]()
    instr.debug_line = l.original_line

    if len(split_content) > 1:
        args = split_content[1:]
        args_res: "list[Argument]" = []

        in_encapsulated_op: bool = False
        cur_encapsulated_op: str = ""

        for idx, arg in enumerate(args):
            actual_part: str = arg[1:]

            if in_encapsulated_op and arg.startswith("("):
                parse_error(
                    "you cannot have an encapsulated operation within another encapsulated operation",
                    {"line": l.original_line, "argument": arg},
                )
            elif not in_encapsulated_op and arg.endswith(")"):
                parse_error(
                    "there is no open encapsulated operation within this instruction - thus, none can be closed",
                    {"line": l.original_line, "argument": arg},
                )

            if arg.startswith("("):
                if cur_encapsulated_op != "":
                    parse_error(
                        "you can only have up to one encapsulated operation per ALU instruction",
                        {"line": l.original_line, "argument": arg},
                    )

                in_encapsulated_op = True
                cur_encapsulated_op += actual_part + " "
                continue

            if arg.endswith(")"):
                in_encapsulated_op = False
                cur_encapsulated_op += arg[:-1]

                split_op = cur_encapsulated_op.split()
                if not split_op[1].startswith("r"):
                    parse_error(
                        "in encapsulated operations, the first operand MUST be a register",
                        {"line": l.original_line, "argument": arg},
                    )

                cur_encapsulated_op = f"{split_op[0]} {str(split_op[1] + ' ') * 2} {' '.join(split_op[2:])}"

                generated_arg: Argument = Argument(
                    0,
                    -1,
                    parse_line(
                        LineOfCode(
                            cur_encapsulated_op,
                            l.original_line,
                            l.part_of,
                            l.rom_addr,
                        ),
                        block_names,
                    ),
                )

                args_res.append(generated_arg)
                continue

            if in_encapsulated_op:
                cur_encapsulated_op += arg + " "
                continue

            if arg.startswith("r") or arg.startswith("$"):
                # register or static address argument!
                reg_to_use: int = -1

                if arg.startswith("r"):
                    if actual_part in ascii_lowercase:
                        reg_to_use = ascii_lowercase.find(actual_part)
                    else:
                        reg_to_use = int(arg[1:])

                    if reg_to_use > (REGISTERS_AVAILABLE - 1):
                        parse_error(
                            f"unavailable register (up to {REGISTERS_AVAILABLE} available)",
                            {
                                "line": l.original_line + 1,
                                "register": reg_to_use,
                            },
                        )

                    elif reg_to_use == -1:
                        parse_error(
                            "unable to resolve register",
                            {"line": l.original_line + 1, "argument": arg},
                        )

                args_res.append(Argument(0, reg_to_use))

            elif arg.startswith("#"):
                # immediate argument!
                immediate_value = int(arg[1:])
                if immediate_value > MAX_INLINE_IMMEDIATE:
                    parse_error(
                        f"inline immediates are limited to {INLINE_IMMEDIATE_BIT_COUNT} bits, so they cannot exceed {MAX_INLINE_IMMEDIATE}.",
                        {"line": l.original_line},
                    )

                args_res.append(Argument(idx, immediate_value))

            elif arg in block_names:
                # jump to named code block is the same as a static address in ROM
                args_res.append(Argument(0, block_names[arg]))

            else:
                parse_error(
                    "invalid argument (must be register, immediate, static address or block name)",
                    {"line": l.original_line + 1, "argument": arg},
                )

        instr.arguments = args_res

    return instr
