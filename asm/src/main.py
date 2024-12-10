from error_handling import debug_info, optimize_debug_info
from bin_generator import generate_binary_from_parsed, write
from parser import build_instructions
from commands import Instruction

from argparse import ArgumentParser

p = ArgumentParser(prog="jcasm", description="Assembler targeting the JoltCore 16 CPU.")
p.add_argument("input_file")
p.add_argument(
    "-o",
    "--output",
    default="./bin.out",
    help="The output file to write the resulting binary to.",
)
p.add_argument(
    "-O",
    "--optimize",
    action="store_true",
    help="Whether to turn on basic optimizations.",
)
p.add_argument(
    "-d",
    "--debug",
    action="store_true",
    help="Whether to generate debug information while compiling.",
)


def main():
    args = p.parse_args()

    if args.debug:
        debug_info("Debug", "enabled debug output")
        if args.optimize:
            optimize_debug_info("optimizations enabled")

    input_file: str = args.input_file
    output_file: str = args.output

    parsed: "list[Instruction]" = build_instructions(
        input_file, args.optimize, args.debug
    )
    write(generate_binary_from_parsed(parsed, args.optimize, args.debug), output_file)


if __name__ == "__main__":
    main()
