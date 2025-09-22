/*
 * 示例C++代码 - 用于AutoGen Studio多智能体分析
 * 文件名: sample_code.cpp
 * 说明: 这个代码包含了多种典型的C++问题，适合测试多智能体分析系统
 */

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <cstring>

// 潜在的安全问题: 缓冲区溢出风险
class UserManager {
private:
    char username[50];
    char password[50];
    bool isAdmin;
    
public:
    // 构造函数 - 存在内存安全问题
    UserManager(const char* user, const char* pass) {
        strcpy(username, user);  // 缓冲区溢出风险
        strcpy(password, pass);  // 缓冲区溢出风险
        isAdmin = false;
    }
    
    // 设置用户名 - 不安全的字符串操作
    void setUsername(const char* user) {
        strcpy(username, user);  // 没有边界检查
    }
    
    // 验证密码 - 弱密码策略
    bool validatePassword(const char* pass) {
        return strcmp(password, pass) == 0;  // 明文密码比较
    }
    
    // 提升权限 - 权限控制漏洞
    void elevateToAdmin(const char* adminCode) {
        if (strcmp(adminCode, "admin123") == 0) {  // 硬编码密码
            isAdmin = true;
        }
    }
    
    // 获取用户信息 - 内存泄漏风险
    char* getUserInfo() {
        char* info = new char[200];  // 可能的内存泄漏
        sprintf(info, "User: %s, Admin: %s", username, isAdmin ? "Yes" : "No");
        return info;  // 调用者需要手动释放内存
    }
};

// 数据处理类 - 算法效率问题
class DataProcessor {
private:
    std::vector<int> data;
    
public:
    // 添加数据 - 效率低下的实现
    void addData(int value) {
        data.push_back(value);
    }
    
    // 查找元素 - O(n)算法，可以优化
    bool findElement(int target) {
        for (size_t i = 0; i < data.size(); i++) {
            if (data[i] == target) {
                return true;
            }
        }
        return false;
    }
    
    // 排序数据 - 使用低效的冒泡排序
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
    
    // 计算统计信息 - 潜在的除零错误
    double calculateAverage() {
        int sum = 0;
        for (int value : data) {
            sum += value;
        }
        return sum / data.size();  // 可能除零
    }
    
    // 数组访问 - 边界检查缺失
    int getElement(int index) {
        return data[index];  // 没有边界检查
    }
};

// 文件操作类 - 资源管理问题
class FileHandler {
private:
    FILE* file;
    char* buffer;
    
public:
    FileHandler() : file(nullptr), buffer(nullptr) {}
    
    // 打开文件 - 缺少错误处理
    void openFile(const char* filename) {
        file = fopen(filename, "r");
        // 没有检查文件是否成功打开
    }
    
    // 读取文件 - 缓冲区溢出和资源泄漏
    void readFile() {
        if (file) {
            buffer = (char*)malloc(1024);
            fread(buffer, 1, 2048, file);  // 读取超过缓冲区大小
            // 没有释放buffer
        }
    }
    
    // 析构函数 - 资源泄漏
    ~FileHandler() {
        // 没有正确关闭文件和释放内存
        // if (file) fclose(file);
        // if (buffer) free(buffer);
    }
};

// 主函数 - 综合问题展示
int main() {
    // 测试用户管理
    UserManager* user = new UserManager("john_doe_with_very_long_username", "super_secret_password_that_is_way_too_long");
    
    // 潜在的空指针解引用
    char* userInfo = user->getUserInfo();
    std::cout << userInfo << std::endl;
    // 内存泄漏: 没有释放userInfo
    
    // 测试数据处理
    DataProcessor processor;
    for (int i = 0; i < 1000; i++) {
        processor.addData(i);
    }
    
    // 可能的除零错误
    double avg = processor.calculateAverage();
    std::cout << "Average: " << avg << std::endl;
    
    // 边界越界访问
    int element = processor.getElement(1500);  // 超出范围
    std::cout << "Element: " << element << std::endl;
    
    // 测试文件处理
    FileHandler handler;
    handler.openFile("nonexistent_file.txt");
    handler.readFile();
    
    // 内存泄漏: 没有释放user
    // delete user;
    
    return 0;
}

/*
 * 代码问题汇总 (供分析师参考):
 * 
 * 安全问题:
 * 1. 缓冲区溢出 (strcpy, sprintf, fread)
 * 2. 硬编码密码
 * 3. 明文密码存储
 * 4. 权限控制不当
 * 
 * 内存管理问题:
 * 1. 内存泄漏 (getUserInfo, buffer, user对象)
 * 2. 资源未释放 (文件句柄)
 * 3. 潜在的空指针解引用
 * 
 * 算法效率问题:
 * 1. 低效排序算法 (冒泡排序)
 * 2. 线性查找可优化为二分查找
 * 3. 字符串操作效率低
 * 
 * 编程实践问题:
 * 1. 缺少边界检查
 * 2. 错误处理不完整
 * 3. 异常安全性差
 * 4. 违反RAII原则
 * 5. 魔术数字使用
 */
