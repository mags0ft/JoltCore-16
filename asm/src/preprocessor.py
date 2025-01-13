import string
from error_handling import preprocess_debug_info, preprocess_error


ALLOWED_DEFINITION_NAMES: str = string.ascii_letters + string.digits + "_"


def remove_comment_from_line(line: str) -> str:
    if line.strip().startswith(";"):
        return ""

    comment_pos = line.find(";")
    return (
        line[: (comment_pos if comment_pos != -1 else len(line))]
        .strip()
        .replace(",", " ")
    )


def comment_out_lines(text: str, lines: set) -> str:
    return "\n".join(
        [
            ("; " if line_idx + 1 in lines else "") + line_content
            for line_idx, line_content in enumerate(text.splitlines())
        ]
    )


def run_preprocessing_passes(text: str, debug_info: bool):
    definitions = {}
    preprocessor_directive_lines = set()

    line, col = 1, 0
    cur = ""
    definition_phase = 0
    cur_definition_name = ""
    cur_definition_content = ""

    for char in text:
        if definition_phase in [1, 2]:
            preprocessor_directive_lines.add(line)

        col += 1
        if char == "\n":
            cur = ""
            line += 1
            col = 1
        elif char == " ":
            cur = ""
        elif char == "{":
            if definition_phase == 1:
                definition_phase = 2
                continue
            elif definition_phase == 2:
                preprocess_error(
                    "you cannot use nested definitions",
                    {"line": line, "col": col, "definition name": cur_definition_name},
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
                        {
                            "line": line,
                            "col": col,
                        },
                    )

                if any(
                    [i not in ALLOWED_DEFINITION_NAMES for i in cur_definition_name]
                ):
                    preprocess_error(
                        f'definitions should only use these characters as names: "{ALLOWED_DEFINITION_NAMES}"',
                        {
                            "line": line,
                            "col": col,
                            "definition name": cur_definition_name,
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

    if debug_info:
        preprocess_debug_info(f"{len(definitions)} definition(s) found")

    passes = 0
    while "!" in "\n".join([remove_comment_from_line(i) for i in text.splitlines()]):
        for key, value in definitions.items():
            text = text.replace(key, value)

        passes += 1

        if passes > 1024:
            preprocess_error(
                "circular reference detected in pre-processing definitions"
            )

    if debug_info:
        preprocess_debug_info(f"{passes} pass(es) done")

    text = comment_out_lines(text, preprocessor_directive_lines)

    return text
