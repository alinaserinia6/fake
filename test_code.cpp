#include <iostream>
#include <cstring>

int main() {
    char buffer[10];
    char input[100];
    
    std::cout << "Enter your name: ";
    std::cin >> input;  // Potential buffer overflow
    
    strcpy(buffer, input);  // Dangerous string copy
    
    std::cout << "Hello, " << buffer << std::endl;
    
    return 0;
}