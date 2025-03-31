#pragma once

#include "file_reader.cpp"
#include <cstdint>
#include <chrono>

class JC16v2CPU
{

public:
    std::vector<FileReader::Command> rom;
    unsigned short ram[1 << 16];

    unsigned short registers[8];
    unsigned short pc = 0;

    unsigned long clock_cycles_passed = 0;
    bool running = true;

    uint16_t alu_last_res;
    bool alu_had_carry;

    void run()
    {
        auto start = std::chrono::high_resolution_clock::now();

        while (running)
        {
            clock_cycle();
        }

        auto end = std::chrono::high_resolution_clock::now();

        std::chrono::duration<double, std::milli> duration = end - start;
        Output::print_info(
            "program execution terminated, took " + std::to_string(clock_cycles_passed) +
            " clock cycle(s) and " + std::to_string(duration.count()) + "ms (avg speed " +
            std::to_string((clock_cycles_passed / (duration.count() / 1000)) / 1000000) + " MIPS)");
    }

    void oclk()
    {
        Output::print_info("oclk");
    }

private:
    void clock_cycle()
    {
        FileReader::Command command = rom.at(pc);
        pc++;

        if (command.is_alu)
        {
            alu_instruction(command);
        }
        else
        {
            switch (command.opcode)
            {
            case 0b10000:
                pc = command.instruction_body;
                break;

            case 0b10001:
                if (alu_last_res == 0)
                {
                    pc = command.instruction_body;
                }
                break;

            case 0b10010:
                if (alu_last_res != 0)
                {
                    pc = command.instruction_body;
                }
                break;

            case 0b10011:
                if (alu_had_carry)
                {
                    pc = command.instruction_body;
                }
                break;

            case 0b10100:
                if (!alu_had_carry)
                {
                    pc = command.instruction_body;
                }
                break;

            case 0b10111:
                oclk();
                break;

            case 0b11000:
                registers[command.target_reg] = command.instruction_body;
                break;

            case 0b11001:
                registers[command.target_reg] = ram[command.instruction_body];
                break;

            case 0b11010:
                ram[command.instruction_body] = registers[command.target_reg];
                break;

            case 0b11011:
                // I/O system not implemented yet; this would be rdpin ...
                break;

            case 0b11100:
                // ... and that would be wrpin!
                break;

            case 0b11111:
                Output::print_info("halt instruction invoked");
                running = false;
                break;

            default:
                Output::print_info("illegal instruction: " + std::to_string(command.opcode));
                running = false;
                break;
            }
        }

        clock_cycles_passed++;
    }

    uint16_t calculate(uint8_t alu_opcode, uint16_t a, uint16_t b, bool main_calculation = false)
    {
        if (main_calculation)
        {
            alu_had_carry = false;
        }

        switch (alu_opcode)
        {
        case 0b0000:
            if (main_calculation && ((uint32_t)a + (uint32_t)b > (1 << 16) - 1))
            {
                alu_had_carry = true;
            }

            return a + b;

        case 0b0001:
            if (main_calculation && (b > a))
            {
                alu_had_carry = true;
            }
            return a - b;

        case 0b0010:
            return a & b;

        case 0b0011:
            return ~a;

        case 0b0100:
            return a | b;

        case 0b0101:
            return a ^ b;

        case 0b0110:
            return ~(a & b);

        case 0b0111:
            return ~(a | b);

        case 0b1000:
            return a << b;

        case 0b1001:
            return a >> b;

        case 0b1010:
            return (a > b) ? 1 : 0;

        case 0b1011:
            return (a < b) ? 1 : 0;

        case 0b1100:
            return (uint16_t)(a == b);

        default:
            return a;
        }
    }

    struct EncapsulatedOperation
    {
        uint8_t alu_opcode;
        uint8_t b;
        bool flag;
    };

    EncapsulatedOperation parse_encapsulated_operation(uint8_t body)
    {
        EncapsulatedOperation res;

        res.alu_opcode = (body & 0b11110000) >> 4;
        res.flag = body & 1;
        res.b = (body & 0b1110) >> 1;
        res.b = (res.flag ? res.b : registers[res.b]);

        return res;
    }

    void alu_instruction(FileReader::Command command)
    {
        uint16_t a, b, res;

        EncapsulatedOperation enc_op = parse_encapsulated_operation(command.alu_body);

        a = registers[command.reg_a];
        b = registers[command.reg_b];

        switch (command.flag)
        {
        case 0b00:
            a = calculate(enc_op.alu_opcode, command.reg_a, enc_op.b);
            break;

        case 0b01:
            b = calculate(enc_op.alu_opcode, command.reg_b, enc_op.b);
            break;

        case 0b10:
            a = command.alu_body;
            break;

        case 0b11:
            b = command.alu_body;
            break;

        default:
            break;
        }

        res = calculate(command.opcode, a, b, true);

        registers[command.target_reg] = res;
        alu_last_res = res;
    }
};
