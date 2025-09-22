#include <iostream>
#include <vector>
#include <string>

// 违反单一职责原则的大类
class DataProcessor {
private:
    std::vector<int> data;
    std::string filename;
    
public:
    // 数据处理
    void process_data() {
        for (auto& item : data) {
            item *= 2;
        }
    }
    
    // 文件操作 (违反SRP)
    void save_to_file() {
        // 文件保存逻辑
    }
    
    // 网络通信 (违反SRP)
    void send_to_server() {
        // 网络发送逻辑
    }
    
    // 日志记录 (违反SRP)
    void log_operation() {
        // 日志记录逻辑
    }
    
    // UI显示 (违反SRP)
    void display_results() {
        // 界面显示逻辑
    }
};

// 高耦合的依赖关系
class DatabaseConnection {
public:
    void connect() { /* ... */ }
    void execute_query(const std::string& sql) { /* ... */ }
};

class UserService {
private:
    DatabaseConnection db;  // 直接依赖具体类，违反DIP
    
public:
    void create_user(const std::string& name) {
        db.connect();  // 紧耦合
        db.execute_query("INSERT INTO users...");
    }
};

// 违反里氏替换原则
class Bird {
public:
    virtual void fly() { /* ... */ }
};

class Penguin : public Bird {
public:
    void fly() override {
        throw std::runtime_error("Penguins can't fly!");  // 违反LSP
    }
};

// 违反接口隔离原则
class AllInOneInterface {
public:
    virtual void print() = 0;
    virtual void scan() = 0;
    virtual void fax() = 0;
    virtual void copy() = 0;
};

class SimplePrinter : public AllInOneInterface {
public:
    void print() override { /* 实现打印 */ }
    void scan() override { /* 不需要但必须实现 */ }
    void fax() override { /* 不需要但必须实现 */ }
    void copy() override { /* 不需要但必须实现 */ }
};

int main() {
    DataProcessor processor;
    processor.process_data();
    processor.save_to_file();
    processor.send_to_server();
    
    return 0;
}
