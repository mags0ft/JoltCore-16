#pragma once

#include "file_reader.cpp"
#include <cstdint>

class JC16v2CPU {

    public:
        std::vector<FileReader::Command> rom;
        unsigned short ram[1<<16];

        unsigned short registers[8];
        unsigned short pc = 0;

        long clock_cycles_passed = 0;
        bool running = true;

        void run() {
            while (running) {
                clock_cycle();
            }
        }

    private:
        void clock_cycle() {
            FileReader::Command command = rom.at(pc);

            switch (command.opcode) {
                case 0b11111:
                    running = false;
                    break;
                
                default:
                    Output::print_info("illegal instruction: " + std::to_string(command.opcode));
                    running = false;
                    break;
            }

            clock_cycles_passed++;
        }

};
