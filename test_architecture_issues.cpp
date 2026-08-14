#include <iostream>
#include <vector>
#include <string>

// Violates the Single Responsibility Principle (SRP)
class DataProcessor {
private:
    std::vector<int> data;
    std::string filename;
    
public:
    // Data processing
    void process_data() {
        for (auto& item : data) {
            item *= 2;
        }
    }
    
    // File operations (violates SRP)
    void save_to_file() {
        // File saving logic
    }
    
    // Network communication (violates SRP)
    void send_to_server() {
        // Network sending logic
    }
    
    // Logging (violates SRP)
    void log_operation() {
        // Logging logic
    }
    
    // UI display (violates SRP)
    void display_results() {
        // UI display logic
    }
};

// Tightly coupled dependencies
class DatabaseConnection {
public:
    void connect() { /* ... */ }
    void execute_query(const std::string& sql) { /* ... */ }
};

class UserService {
private:
    DatabaseConnection db;  // Direct dependency on concrete class, violates DIP
    
public:
    void create_user(const std::string& name) {
        db.connect();  // Tight coupling
        db.execute_query("INSERT INTO users...");
    }
};

// Violates the Liskov Substitution Principle (LSP)
class Bird {
public:
    virtual void fly() { /* ... */ }
};

class Penguin : public Bird {
public:
    void fly() override {
        throw std::runtime_error("Penguins can't fly!");  // Violates LSP
    }
};

// Violates the Interface Segregation Principle (ISP)
class AllInOneInterface {
public:
    virtual void print() = 0;
    virtual void scan() = 0;
    virtual void fax() = 0;
    virtual void copy() = 0;
};

class SimplePrinter : public AllInOneInterface {
public:
    void print() override { /* Implement printing */ }
    void scan() override { /* Not needed but must implement */ }
    void fax() override { /* Not needed but must implement */ }
    void copy() override { /* Not needed but must implement */ }
};

int main() {
    DataProcessor processor;
    processor.process_data();
    processor.save_to_file();
    processor.send_to_server();
    
    return 0;
}