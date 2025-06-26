#pragma once

#include <iostream>

namespace Output
{

    void print_info(std::string info, bool omit_info = false)
    {
        // Method for handling formatted printing
        std::cout << (omit_info ? "" : "jcemu: ") << info << std::endl;
    }

}
