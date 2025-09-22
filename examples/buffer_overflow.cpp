/*
 * 示例1: 缓冲区溢出漏洞
 * 包含多种缓冲区溢出风险
 */

#include <iostream>
#include <cstring>
#include <stdio.h>

class UserManager {
private:
    char username[32];
    char password[16];
    
public:
    void setCredentials(const char* user, const char* pass) {
        // 危险：没有边界检查的strcpy
        strcpy(username, user);  // 潜在缓冲区溢出
        strcpy(password, pass);  // 潜在缓冲区溢出
    }
    
    void printUserInfo() {
        printf("User: %s\n", username);  // 格式字符串漏洞风险
    }
    
    bool authenticate(char* inputUser, char* inputPass) {
        char tempBuffer[64];
        
        // 危险：gets函数已被弃用，存在缓冲区溢出风险
        printf("Enter additional info: ");
        gets(tempBuffer);  // 严重安全漏洞
        
        // 不安全的字符串比较
        if (strcmp(username, inputUser) == 0 && 
            strcmp(password, inputPass) == 0) {
            return true;
        }
        
        return false;
    }
};

int main() {
    UserManager user;
    
    // 模拟长用户名和密码输入
    char longUsername[] = "this_is_a_very_long_username_that_exceeds_buffer_size_and_causes_overflow";
    char longPassword[] = "extremely_long_password_string";
    
    // 这里会发生缓冲区溢出
    user.setCredentials(longUsername, longPassword);
    
    user.printUserInfo();
    
    // 模拟用户输入验证
    char inputUser[100], inputPass[100];
    printf("Username: ");
    scanf("%99s", inputUser);  // 稍微安全一些，但仍有风险
    printf("Password: ");
    scanf("%99s", inputPass);
    
    if (user.authenticate(inputUser, inputPass)) {
        std::cout << "Authentication successful!" << std::endl;
    } else {
        std::cout << "Authentication failed!" << std::endl;
    }
    
    return 0;
}
