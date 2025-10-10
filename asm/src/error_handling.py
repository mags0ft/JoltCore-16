"""
This module takes care of printing out errors and warnings in a unified manner.
Colorama is used to make outputs visually appealing.
"""

import sys
from colorama import Fore


# to circumvent python's missing feature to use escape sequences inside of f-strings before 3.12
NEWLINE_ERROR_SEPERATOR = "\n    "


def error(title: str, description: str, info: dict = {}):
    """
    Function handling errors that are fatal, terminating assembly.
    Forces an exit with code 1.
    """
    
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
    """
    Merely prints some debug information.
    """
    
    print(
        f"{Fore.LIGHTGREEN_EX}Debug{Fore.RESET} {Fore.BLUE}{title}{Fore.RESET}: {Fore.CYAN}{info}{Fore.RESET}"
    )


def codegen_debug_info(info: str):
    """
    Prints debug information in the code generation step.
    """
    
    debug_info("Code generation", info)


def preprocess_debug_info(info: str):
    """
    Prints debug information in the pre-processing step.
    """
    
    debug_info("Pre-processing", info)


def parse_debug_info(info: str):
    """
    Prints debug information in the parsing step.
    """
    
    debug_info("Parser", info)


def optimize_debug_info(info: str):
    """
    Prints debug information in the optimization step.
    """
    
    debug_info("Optimization", info)


def codegen_error(description: str, info: dict = {}):
    """
    Throws an error in the code generation step.
    """
    
    error("Code generation failed", description, info)


def preprocess_error(description: str, info: dict = {}):
    """
    Throws an error in the pre-processing step.
    """
    
    error("Pre-processing", description, info)


def parse_error(description: str, info: dict = {}):
    """
    Throws an error in the parsing step.
    """
    
    error("Couldn't parse the assembly file", description, info)
