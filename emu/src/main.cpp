#include "file_reader.cpp"
#include "jc16v2_cpu.cpp"
#include "output.cpp"
#include "config.cpp"

int main(int argc, char* argv[]) {
    Output::print_info("version " + Config::VERSION);

    if (argc < 2) {
        Output::print_info("usage: ./jcemu [filename]");
        return -1;
    }

    std::string filename_to_read = argv[1];
    std::vector<FileReader::Command> commands = FileReader::read_file(filename_to_read);

    JC16v2CPU cpu;

    cpu.rom = commands;
    cpu.run();

    return 0;
}
