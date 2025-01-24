from typing import Union
from spec import INLINE_IMMEDIATE_BIT_COUNT, MAX_INT
from error_handling import codegen_error, optimize_debug_info


class Argument:
    # 0 = register or encapsulated operation, 1 = immediate for arg 0, 2 = immediate for arg 1
    type_: int = 0
    # value is either the register to target or the immediate itself
    value: int = 0

    encapsulated_operation: "Union[ALUInstruction, None]" = None

    def __init__(self, type_, value, encapsulated_operation=None):
        self.type_ = type_
        self.value = value
        self.encapsulated_operation = encapsulated_operation

    def generate_binary(self):
        if self.encapsulated_operation != None:
            return f"{self.encapsulated_operation.arguments[0].value:03b}"

        return ("{0:03b}".format(self.value)) if self.type_ == 0 else "000"

    def get_immediate(self):
        return f"{(0 if self.type_ == 0 else self.value):08b}"

    def get_immediate_flag(self):
        # type + 1, because the flags mean this:
        # 00 = encapsulated operation applied to operand A
        # 01 = encapsulated operation applied to operand B
        # 10 = inline immediate parameter instead of operand A
        # 11 = inline immediate parameter instead of operand B

        return f"{self.type_+1:02b}"

    def get_encapsulated_operation_binary(self):
        if self.encapsulated_operation == None:
            return f"{NOP.opcode[1:]} 000 0"

        if isinstance(self.encapsulated_operation, BitwiseNot):
            # edge case: NOT only has one operand, the register, and nothing else
            return f"{self.encapsulated_operation.opcode[1:]} 000 0"

        # arguments[1] is the register B of the encapsulated operation, register A is the register
        # the encapsulated operation is being applied to
        return (
            f"{self.encapsulated_operation.opcode[1:]} "
            + f"{self.encapsulated_operation.arguments[2].value:03b} "
            + f"{'1' if self.encapsulated_operation.arguments[2].type_ != 0 else '0'}"
        )

    def __str__(self):
        type_description: str = (
            "register"
            if self.type_ == 0
            else "immediate for operand " + "AB"[self.type_ - 1]
        )
        value_description: str = ""
        if self.encapsulated_operation == None:
            value_description = str(self.value)
        else:
            value_description = (
                self.encapsulated_operation.legible_name
                + " "
                + (",".join([str(i) for i in self.encapsulated_operation.arguments]))
            )

        return f'<Argument ({type_description}) "{value_description}">'


class Instruction:
    # information for raised errors
    debug_line: int = -1
    legible_name: str = "instruction"

    def right_num_of_args(self, num: int) -> bool:
        return num == 0

    # information for compilation
    opcode: str = "00000"
    arguments: "list[Argument]" = []

    def raise_error(self, description):
        codegen_error(
            description,
            {
                "line": (
                    str(self.debug_line + 1) if self.debug_line != -1 else "unknown"
                ),
                "instruction": self.legible_name,
            },
        )

    def is_omitable(self) -> bool:
        # function to return true if the instruction does not perform anything
        # (this may be the case with an addition with #0, for example)
        return False

    def generate_binary(self, optimize: bool = False, debug_info: bool = False):
        # returns the generated binary as a string
        if optimize and self.is_omitable():
            if debug_info:
                optimize_debug_info(
                    f"instruction on line {self.debug_line + 1} omitted (it doesn't do anything)"
                )
            return ""

        if not self.right_num_of_args(len(self.arguments)):
            self.raise_error(
                f"command has wrong amount of arguments, got {len(self.arguments)}"
            )

        determined_flag: str = "00"
        determined_immediate: str = ""
        determined_encapsulated_operation: str = ""

        compiled_args: str = ""
        for idx, arg in enumerate(self.arguments):
            if arg.type_ != 0:
                if arg.encapsulated_operation != None:
                    self.raise_error(
                        "cannot have immediate and encapsulated operation at the same time"
                    )
                elif idx == 0:
                    self.raise_error("output register cannot be an immediate")
                elif determined_flag != "00" or determined_immediate:
                    self.raise_error(
                        "cannot use two immediates inside of one instruction"
                    )

                # Oh! We have an immediate right here.
                determined_flag = arg.get_immediate_flag()
                determined_immediate = arg.get_immediate()
            elif arg.encapsulated_operation != None:
                determined_flag = f"{idx - 1:02b}"
                determined_encapsulated_operation = (
                    arg.get_encapsulated_operation_binary()
                )

            compiled_args += arg.generate_binary() + " "

        if isinstance(self, ALUInstruction):
            if (
                determined_flag == "00"
                and (not determined_immediate)
                and (not determined_encapsulated_operation)
            ):
                # Okay - we seem to have a very plain instruction here; one that doesn't
                # make use of inline immediates and also doesn't work with any encapsulated
                # operations. Thus, we need to creaty a "dummy" encapsulated operation that
                # simply doesn't do anything with our input values so that our CPU can work
                # with the instruction.

                determined_encapsulated_operation = f"{NOP.opcode[1:]} 000 0"
        else:
            determined_flag = ""
            determined_encapsulated_operation = ""
            determined_immediate = ""

        return (
            f"{self.opcode} {' '.join([i.generate_binary() for i in self.arguments])} "
            + f"{determined_flag} "
            + (
                determined_immediate
                if determined_flag.startswith("1")
                else determined_encapsulated_operation
            )
        ).strip()


class ALUInstruction(Instruction):
    legible_name: str = "ALU (Arithmetic/Logic Unit) instruction"
    opcode: str = "00000"

    def right_num_of_args(self, num: int):
        return num == 3  # one output, two operands


class Add(ALUInstruction):
    legible_name: str = "Integer addition"
    opcode: str = "00000"

    def is_omitable(self) -> bool:
        # addition with a #0 will always result in the same value as before.
        # If we do now write this same value into the same register as it is also
        # coming from, we essentially do nothing. Therefore, we can omit the command.

        target_reg = self.arguments[0]
        source_reg = (
            self.arguments[1] if self.arguments[1].type_ == 0 else self.arguments[2]
        )

        return target_reg.value == source_reg.value and any(
            [(arg.type_ != 0 and arg.value == 0) for arg in self.arguments[1:]]
        )


class Subtract(ALUInstruction):
    legible_name: str = "Integer subtraction"
    opcode: str = "00001"

    def is_omitable(self) -> bool:
        # subtracting by zero doesn't do anything
        target_reg = self.arguments[0]
        source_reg = self.arguments[1]
        last_arg = self.arguments[2]

        # we have to be careful here - we can only omit this command
        # if it would write into the same register as before and result
        # in the same value.
        return (
            last_arg.type_ != 0
            and last_arg.value == 0
            and source_reg.type_ == 0
            and target_reg.value == source_reg.value
        )


class BitwiseAnd(ALUInstruction):
    legible_name: str = "Bitwise-AND"
    opcode: str = "00010"


class BitwiseNot(ALUInstruction):
    legible_name: str = "Bitwise-NOT"
    opcode: str = "00011"

    def right_num_of_args(self, num: int):
        return num == 2  # one output, one operand


class BitwiseOr(ALUInstruction):
    legible_name: str = "Bitwise-OR"
    opcode: str = "00100"


class BitwiseXor(ALUInstruction):
    legible_name: str = "Bitwise-XOR"
    opcode: str = "00101"


class BitwiseNand(ALUInstruction):
    legible_name: str = "Bitwise-NAND"
    opcode: str = "00110"


class BitwiseNor(ALUInstruction):
    legible_name: str = "Bitwise-NOR"
    opcode: str = "00111"


class ShiftInstruction(ALUInstruction):
    legible_name: str = "Shift operation"
    opcode: str = "01000"

    def is_omitable(self) -> bool:
        # shifting by zero doesn't do anything
        target_reg = self.arguments[0]
        source_reg = self.arguments[1]
        last_arg = self.arguments[2]

        # we can only omit if we are writing into the same register as
        # we are reading from and shifting by no more than exactly 0 bits
        return (
            last_arg.type_ != 0
            and last_arg.value == 0
            and source_reg.type_ == 0
            and target_reg.value == source_reg.value
        )


class LeftShift(ShiftInstruction):
    legible_name: str = "Binary left-shift"


class RightShift(ShiftInstruction):
    legible_name: str = "Binary right-shift"
    opcode: str = "01001"


class GreaterThan(ALUInstruction):
    legible_name: str = "Greater than-comparison"
    opcode: str = "01010"


class LessThan(ALUInstruction):
    legible_name: str = "Less than-comparison"
    opcode: str = "01011"


class IsEquals(ALUInstruction):
    legible_name: str = "Equals-comparison"
    opcode: str = "01100"


class NOP(ALUInstruction):
    legible_name: str = "No operation"
    opcode: str = "01111"


class JumpInstruction(Instruction):
    legible_name: str = "Jump-like instruction"
    opcode: str = "10000"

    def right_num_of_args(self, num: int):
        return num == 1  # one NULL, one address


class Jump(JumpInstruction):
    legible_name: str = "Jump instruction"

    def generate_binary(self, optimize: bool = False, debug_info: bool = False):
        return f"{self.opcode} 000 {self.arguments[0].value:016b}"


class JumpIfZero(Jump):
    legible_name: str = (
        "Conditional jump only if the last ALU operation resulted in zero"
    )
    opcode: str = "10001"


class JumpIfNotZero(Jump):
    legible_name: str = (
        "Conditional jump only if the last ALU operation did not result in zero"
    )
    opcode: str = "10010"


class JumpIfCarry(Jump):
    legible_name: str = "Conditional jump only if the last ALU operation had a carry"
    opcode: str = "10011"


class JumpIfNoCarry(Jump):
    legible_name: str = (
        "Conditional jump only if the last ALU operation did not have a carry"
    )
    opcode: str = "10100"


class OutputClockSignal(Instruction):
    legible_name: str = "Emit a signal to CLK"
    opcode: str = "10111"


class LDI(Instruction):
    legible_name: str = "Load an immediate"
    opcode: str = "11000"

    def right_num_of_args(self, num: int):
        return num == 2  # target register, one immediate

    def generate_binary(self, optimize: bool = False, debug_info: bool = False):
        if (not self.right_num_of_args(len(self.arguments))) or (
            self.arguments[1].type_ != 1
        ):
            self.raise_error(
                "the LDI command only expects exactly one immediate",
            )
        return f"{self.opcode} 000 {self.arguments[1].value:016b}"


class LoadFromRAM(Instruction):
    legible_name: str = "Load a value from RAM into a register"
    opcode: str = "11001"

    def right_num_of_args(self, num: int):
        return num == 2  # target register, one address


class StoreInRAM(Instruction):
    legible_name: str = "Write from register into RAM"
    opcode: str = "11010"

    def right_num_of_args(self, num: int):
        return num == 2  # source register, one address


class ReadFromPin(Instruction):
    legible_name: str = "Read from pin"
    opcode: str = "11011"

    def right_num_of_args(self, num: int):
        return num == 2  # target register, one immediate


class WriteToPin(Instruction):
    legible_name: str = "Write to pin"
    opcode: str = "11100"

    def right_num_of_args(self, num: int):
        return num == 2  # source register, one immediate


class Halt(Instruction):
    legible_name: str = "Terminate the program"
    opcode: str = "11111"


COMMANDS = {
    "add": Add,
    "sub": Subtract,
    "and": BitwiseAnd,
    "not": BitwiseNot,
    "or": BitwiseOr,
    "xor": BitwiseXor,
    "nand": BitwiseNand,
    "nor": BitwiseNor,
    "lshift": LeftShift,
    "rshift": RightShift,
    "gt": GreaterThan,
    "lt": LessThan,
    "eq": IsEquals,
    "nop": NOP,
    "jmp": Jump,
    "jiz": JumpIfZero,
    "jnz": JumpIfNotZero,
    "jic": JumpIfCarry,
    "jnc": JumpIfNoCarry,
    "oclk": OutputClockSignal,
    "ldi": LDI,
    "ldram": LoadFromRAM,
    "stram": StoreInRAM,
    "rdpin": ReadFromPin,
    "wrpin": WriteToPin,
    "halt": Halt,
}
