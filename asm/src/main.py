#!/usr/bin/python3

"""
The main module for JCASM; handles argument parsing and controls the general
flow of the assembler.
"""

from error_handling import debug_info, optimize_debug_info, error
from bin_generator import generate_build_from_parsed, write
from parser import build_instructions
from commands import Instruction
from spec import OUTPUT_EXTENSIONS

from argparse import ArgumentParser


def main():
    """
    The main entry point for JCASM; parses arguments, builds instructions,
    generates binaries, and writes them to disk. Controls the general flow of
    the assembler.
    """

    p = ArgumentParser(
        prog="jcasm", description="Assembler targeting the JoltCore 16 CPU."
    )
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
        "-f",
        "--format",
        help=f"Which format(s) to use when exporting (possible: {', '.join(OUTPUT_EXTENSIONS.keys())})",
        default="brx",
    )
    p.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Whether to generate debug information while compiling.",
    )
    p.add_argument(
        "--noext",
        action="store_true",
        help="Whether to leave out the format-specific extension (only works when building for one format)",
    )

    args = p.parse_args()

    for char in args.format:
        if char not in OUTPUT_EXTENSIONS:
            error("jcasm", f'unknown output format "{char}"')

    if len(args.format) > len(OUTPUT_EXTENSIONS) or len(args.format) == 0:
        error("jcasm", "invalid number of requested output formats")

    if args.noext and len(args.format) != 1:
        error(
            "jcasm",
            "--format needs to specify exactly one output format when using --noext.",
        )

    if args.debug:
        debug_info("Debug", "enabled debug output")
        if args.optimize:
            optimize_debug_info("optimizations enabled")

    input_file: str = args.input_file
    output_file: str = args.output

    parsed: "list[Instruction]" = build_instructions(
        input_file, args.optimize, args.debug, args
    )

    for build, extension, binary in generate_build_from_parsed(
        parsed, args.format, args.optimize, args.debug
    ):
        write(
            build,
            output_file + (f".{extension}" if not args.noext else ""),
            binary,
        )


if __name__ == "__main__":
    main()
