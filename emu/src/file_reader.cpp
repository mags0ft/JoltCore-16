#pragma once

#include "output.cpp"

#include <cstdint>
#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>

namespace FileReader
{

    struct Command
    {
        uint8_t opcode;
        uint8_t target_reg;

        bool is_alu;

        // for ALU-specific commands:
        uint8_t flag;
        uint8_t reg_a;
        uint8_t reg_b;
        uint8_t alu_body;
        bool has_encapsulated_op;

        // for other commands:
        uint16_t instruction_body;
    };

    Command decode_instruction(uint32_t instruction)
    {
        Command res;

        res.opcode = (instruction & (0x1F << 19)) >> 19;
        res.is_alu = !(bool)(instruction & (1 << 23));
        res.target_reg = (instruction & (7 << 16)) >> 16;

        if (res.is_alu)
        {
            res.has_encapsulated_op = instruction & (1 << 9);
            res.alu_body = instruction & 0xFF;
            res.flag = (instruction & 0x300) >> 8;
            res.reg_a = (instruction & (7 << 13)) >> 13;
            res.reg_b = (instruction & (7 << 10)) >> 10;
        }

        res.instruction_body = instruction & 0xFFFF;

        return res;
    }

    std::vector<Command> read_file(std::string filename)
    {
        std::vector<Command> res;

        std::ifstream file(filename, std::ios::binary);

        if (!file)
        {
            Output::print_info("cannot open file");
            std::exit(1);
        }

        while (true)
        {
            uint8_t buffer[3];
            uint32_t instruction = 0;

            file.read(reinterpret_cast<char *>(buffer), 3);

            instruction |= (static_cast<uint32_t>(buffer[2]) << 16);
            instruction |= (static_cast<uint32_t>(buffer[1]) << 8);
            instruction |= static_cast<uint32_t>(buffer[0]);

            res.push_back(decode_instruction(instruction));

            if (file.gcount() != 3)
            {
                break;
            }
        }

        file.close();

        return res;
    }

}
