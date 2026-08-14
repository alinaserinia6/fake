/*
 * Example 1: Buffer Overflow Vulnerability
 * Contains multiple buffer overflow risks
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
        // Dangerous: strcpy without boundary checking
        strcpy(username, user);  // Potential buffer overflow
        strcpy(password, pass);  // Potential buffer overflow
    }
    
    void printUserInfo() {
        printf("User: %s\n", username);  // Format string vulnerability risk
    }
    
    bool authenticate(char* inputUser, char* inputPass) {
        char tempBuffer[64];
        
        // Dangerous: gets function is deprecated, poses buffer overflow risk
        printf("Enter additional info: ");
        gets(tempBuffer);  // Critical security vulnerability
        
        // Unsafe string comparison
        if (strcmp(username, inputUser) == 0 && 
            strcmp(password, inputPass) == 0) {
            return true;
        }
        
        return false;
    }
};

int main() {
    UserManager user;
    
    // Simulate long username and password input
    char longUsername[] = "this_is_a_very_long_username_that_exceeds_buffer_size_and_causes_overflow";
    char longPassword[] = "extremely_long_password_string";
    
    // Buffer overflow will occur here
    user.setCredentials(longUsername, longPassword);
    
    user.printUserInfo();
    
    // Simulate user input validation
    char inputUser[100], inputPass[100];
    printf("Username: ");
    scanf("%99s", inputUser);  // Somewhat safer, but still risky
    printf("Password: ");
    scanf("%99s", inputPass);
    
    if (user.authenticate(inputUser, inputPass)) {
        std::cout << "Authentication successful!" << std::endl;
    } else {
        std::cout << "Authentication failed!" << std::endl;
    }
    
    return 0;
}
