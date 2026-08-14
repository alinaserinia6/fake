/*
 * Example C++ code - For AutoGen Studio multi-agent analysis
 * Filename: sample_code.cpp
 * Description: This code contains multiple typical C++ issues, suitable for testing the multi-agent analysis system
 */

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <cstring>

// Potential security issue: Buffer overflow risk
class UserManager {
private:
    char username[50];
    char password[50];
    bool isAdmin;
    
public:
    // Constructor - has memory safety issues
    UserManager(const char* user, const char* pass) {
        strcpy(username, user);  // Buffer overflow risk
        strcpy(password, pass);  // Buffer overflow risk
        isAdmin = false;
    }
    
    // Set username - unsafe string operation
    void setUsername(const char* user) {
        strcpy(username, user);  // No boundary checking
    }
    
    // Validate password - weak password policy
    bool validatePassword(const char* pass) {
        return strcmp(password, pass) == 0;  // Plaintext password comparison
    }
    
    // Elevate privileges - privilege control vulnerability
    void elevateToAdmin(const char* adminCode) {
        if (strcmp(adminCode, "admin123") == 0) {  // Hard-coded password
            isAdmin = true;
        }
    }
    
    // Get user info - memory leak risk
    char* getUserInfo() {
        char* info = new char[200];  // Potential memory leak
        sprintf(info, "User: %s, Admin: %s", username, isAdmin ? "Yes" : "No");
        return info;  // Caller must manually free memory
    }
};

// Data processing class - algorithm efficiency issues
class DataProcessor {
private:
    std::vector<int> data;
    
public:
    // Add data - inefficient implementation
    void addData(int value) {
        data.push_back(value);
    }
    
    // Find element - O(n) algorithm, can be optimised
    bool findElement(int target) {
        for (size_t i = 0; i < data.size(); i++) {
            if (data[i] == target) {
                return true;
            }
        }
        return false;
    }
    
    // Sort data - uses inefficient bubble sort
    void sortData() {
        int n = data.size();
        for (int i = 0; i < n-1; i++) {
            for (int j = 0; j < n-i-1; j++) {
                if (data[j] > data[j+1]) {
                    int temp = data[j];
                    data[j] = data[j+1];
                    data[j+1] = temp;
                }
            }
        }
    }
    
    // Calculate statistics - potential division by zero
    double calculateAverage() {
        int sum = 0;
        for (int value : data) {
            sum += value;
        }
        return sum / data.size();  // Possible division by zero
    }
    
    // Array access - missing boundary checking
    int getElement(int index) {
        return data[index];  // No boundary checking
    }
};

// File operation class - resource management issues
class FileHandler {
private:
    FILE* file;
    char* buffer;
    
public:
    FileHandler() : file(nullptr), buffer(nullptr) {}
    
    // Open file - missing error handling
    void openFile(const char* filename) {
        file = fopen(filename, "r");
        // No check for successful file opening
    }
    
    // Read file - buffer overflow and resource leak
    void readFile() {
        if (file) {
            buffer = (char*)malloc(1024);
            fread(buffer, 1, 2048, file);  // Reading more than buffer size
            // buffer is not freed
        }
    }
    
    // Destructor - resource leaks
    ~FileHandler() {
        // File not properly closed and memory not freed
        // if (file) fclose(file);
        // if (buffer) free(buffer);
    }
};

// Main function - comprehensive issue demonstration
int main() {
    // Test user management
    UserManager* user = new UserManager("john_doe_with_very_long_username", "super_secret_password_that_is_way_too_long");
    
    // Potential null pointer dereference
    char* userInfo = user->getUserInfo();
    std::cout << userInfo << std::endl;
    // Memory leak: userInfo not freed
    
    // Test data processing
    DataProcessor processor;
    for (int i = 0; i < 1000; i++) {
        processor.addData(i);
    }
    
    // Possible division by zero
    double avg = processor.calculateAverage();
    std::cout << "Average: " << avg << std::endl;
    
    // Out-of-bounds access
    int element = processor.getElement(1500);  // Out of range
    std::cout << "Element: " << element << std::endl;
    
    // Test file handling
    FileHandler handler;
    handler.openFile("nonexistent_file.txt");
    handler.readFile();
    
    // Memory leak: user not freed
    // delete user;
    
    return 0;
}

/*
 * Code issue summary (for analyst reference):
 *
 * Security issues:
 * 1. Buffer overflow (strcpy, sprintf, fread)
 * 2. Hard-coded password
 * 3. Plaintext password storage
 * 4. Insecure privilege control
 *
 * Memory management issues:
 * 1. Memory leaks (getUserInfo, buffer, user object)
 * 2. Unreleased resources (file handles)
 * 3. Potential null pointer dereference
 *
 * Algorithm efficiency issues:
 * 1. Inefficient sorting algorithm (bubble sort)
 * 2. Linear search could be optimised to binary search
 * 3. Inefficient string operations
 *
 * Programming practice issues:
 * 1. Missing boundary checking
 * 2. Incomplete error handling
 * 3. Poor exception safety
 * 4. RAII principle violations
 * 5. Magic number usage
 */
