import sys
from colorama import Fore


# to circumvent python's missing feature to use escape sequences inside of f-strings before 3.12
NEWLINE_ERROR_SEPERATOR = "\n    "


def error(title: str, description: str, info: dict = {}):
    print(
        f"""{Fore.RED}Error{Fore.RESET}: {Fore.LIGHTRED_EX}{title}{Fore.RESET}
    {description}

{Fore.CYAN}Error details{Fore.RESET}:
    {(NEWLINE_ERROR_SEPERATOR.join([k + ": " + str(v) for k, v in info.items()])) if info else (Fore.GREEN + "(none)" + Fore.RESET)}

{Fore.RED}Program assembly terminated.{Fore.RESET}
"""
    )
    sys.exit(1)


def debug_info(title: str, info: str):
    print(
        f"{Fore.LIGHTGREEN_EX}Debug{Fore.RESET} {Fore.BLUE}{title}{Fore.RESET}: {Fore.CYAN}{info}{Fore.RESET}"
    )


def codegen_debug_info(info: str):
    debug_info("Code generation", info)


def preprocess_debug_info(info: str):
    debug_info("Pre-processing", info)


def parse_debug_info(info: str):
    debug_info("Parser", info)


def optimize_debug_info(info: str):
    debug_info("Optimization", info)


def codegen_error(description: str, info: dict = {}):
    error("Code generation failed", description, info)


def preprocess_error(description: str, info: dict = {}):
    error("Pre-processing", description, info)


def parse_error(description: str, info: dict = {}):
    error("Couldn't parse the assembly file", description, info)
