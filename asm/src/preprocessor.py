"""
Preprocessor module for JCASM; handles preprocessing directives such as
includes and definitions to allow for more complex assembly source code with
higher levels of abstraction.
"""

import string
from uuid import uuid4
from bin_generator import write
from error_handling import preprocess_debug_info, preprocess_error

ALLOWED_DEFINITION_NAMES: str = string.ascii_letters + string.digits + "_"
INCLUDE_KEYWORD: str = "include "


def remove_comment_from_line(line: str) -> str:
    """
    Removes comments from a single line of code.
    """

    if line.strip().startswith(";"):
        return ""

    comment_pos = line.find(";")
    return (
        line[: (comment_pos if comment_pos != -1 else len(line))]
        .strip()
        .replace(",", " ")
    )


def comment_out_lines(text: str, lines: set) -> str:
    """
    Comments out the specified lines in the given text (adds ";" at the start
    of each line).
    """

    return "\n".join(
        [
            ("; " if line_idx + 1 in lines else "") + line_content
            for line_idx, line_content in enumerate(text.splitlines())
        ]
    )


def run_preprocessing_passes(
    text: str, debug_info: bool, file: str, args=None
):
    """
    Runs the preprocessing passes on the given text.
    """

    definitions = parse_directives(text, debug_info, file)

    if debug_info:
        preprocess_debug_info(f"{len(definitions)} definition(s) found")

    def remove_preprocessed_lines():
        return "\n".join(
            [
                remove_comment_from_line(i)
                for i in comment_out_lines(
                    text, find_preprocessor_directive_lines(text)
                ).splitlines()
            ]
        )

    passes = 0
    while "!" in remove_preprocessed_lines():
        for key, value in definitions.items():
            while True:
                uuid: str = str(uuid4()).replace("-", "_")

                altered_value = value.replace("scope!", uuid)

                prev_text: str = text
                text = text.replace(key, altered_value, 1)

                if prev_text == text:
                    break

        passes += 1

        if passes > 1024:
            t = [i.strip() for i in remove_preprocessed_lines().split()]
            preprocess_error(
                "undefined definition or circular reference detected in pre-processing definitions"
                "\n    affected definitions: \n\t- "
                + "\n\t- ".join(filter(lambda s: s.endswith("!"), t))
            )

    if debug_info:
        preprocess_debug_info(f"{passes} pass(es) done")

    text = comment_out_lines(text, find_preprocessor_directive_lines(text))

    if args is not None and "p" in args.format:
        write(text, args.output + (f".asm" if not args.noext else ""), False)

    return text


def find_preprocessor_directive_lines(text):
    """
    Finds all lines that contain preprocessor directives and returns their
    line numbers as a set.
    """

    lines: "set[int]" = set()
    line: int = 0

    in_comment: bool = False
    in_definition: bool = False

    cur_line: str = ""

    for char in text:
        cur_line += char

        if char == "\n":
            if in_definition:
                lines.add(line)

            line += 1
            in_comment = False

            if cur_line.strip().startswith(INCLUDE_KEYWORD):
                lines.add(line)

            cur_line = ""
        elif char == ";":
            in_comment = True
        elif char == "{" and not in_comment:
            in_definition = True
        elif char == "}" and not in_comment:
            in_definition = False
            lines.update([line, line + 1])

    return lines


def parse_directives(text: str, debug_info: bool, file: str):
    """
    Parses the preprocessing directives in the given text and returns a
    dictionary mapping definition names to their contents.
    """

    definitions: "dict[str, str]" = {}

    line: int = 1
    col: int = 0
    cur: str = ""

    in_comment: bool = False
    definition_phase: int = 0
    cur_definition_name: str = ""
    cur_definition_content: str = ""

    # FILE INCLUDES

    for line_idx, line_ in enumerate([i.strip() for i in text.splitlines()]):
        if line_.startswith(INCLUDE_KEYWORD):
            filename: str = line_[len(INCLUDE_KEYWORD) :]
            try:
                with open(filename, "r") as f:
                    included_file_data = f.read()

                if debug_info:
                    preprocess_debug_info(f'including file "{filename}"')

                definitions.update(
                    parse_directives(included_file_data, debug_info, filename)
                )

            except FileNotFoundError:
                preprocess_error(
                    f'cannot include file "{filename}": file not found',
                    {"line": line_idx + 1, "in file": file},
                )

    # DEFINITIONS

    for char in text:
        if char == ";":
            in_comment = True

        col += 1
        if char == "\n":
            cur = ""
            line += 1
            col = 1
            in_comment = False
        elif in_comment:
            continue
        elif char == " ":
            cur = ""
        elif char == "{":
            if definition_phase == 1:
                definition_phase = 2
                continue
            elif definition_phase == 2:
                preprocess_error(
                    "you cannot use nested definitions",
                    {
                        "line": line,
                        "col": col,
                        "definition name": cur_definition_name,
                        "in file": file,
                    },
                )
            else:
                preprocess_error('stray "{"', {"line": line, "col": col})

        if definition_phase == 1:
            cur_definition_name += char
        elif definition_phase == 2:
            if char == "}":
                definition_phase = 0

                cur_definition_name = cur_definition_name.strip()
                cur_definition_content = cur_definition_content.strip()

                if cur_definition_name in definitions:
                    preprocess_error(
                        f'you already defined "{cur_definition_name}"',
                        {"line": line, "col": col, "in file": file},
                    )

                if any(
                    [
                        i not in ALLOWED_DEFINITION_NAMES
                        for i in cur_definition_name
                    ]
                ):
                    preprocess_error(
                        f'definitions should only use these characters as names: "{ALLOWED_DEFINITION_NAMES}"',
                        {
                            "line": line,
                            "col": col,
                            "definition name": cur_definition_name,
                            "in file": file,
                        },
                    )

                definitions[cur_definition_name + "!"] = cur_definition_content

                cur_definition_content = ""
                cur_definition_name = ""
                cur = ""
                continue

            cur_definition_content += char
            continue

        else:
            cur += char

        if cur.strip() == "define":
            definition_phase = 1
            cur_definition_content = ""
            cur_definition_name = ""
            cur = ""

    return definitions
