#include <iostream>
#include <cstring>

int main() {
    char buffer[10];
    char input[100];
    
    std::cout << "Enter your name: ";
    std::cin >> input;  // 潜在的缓冲区溢出
    
    strcpy(buffer, input);  // 危险的字符串复制
    
    std::cout << "Hello, " << buffer << std::endl;
    
    return 0;
}
