/*
 * 示例4: 复杂架构问题
 * 包含设计模式误用、高耦合、职责不明确等问题
 */

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>

// 违反单一职责原则的巨型类
class MegaClass {
private:
    std::string name;
    std::vector<int> data;
    std::map<std::string, double> cache;
    bool isValid;
    int errorCode;
    
public:
    // 构造函数做了太多事情
    MegaClass(const std::string& n) : name(n), isValid(false), errorCode(0) {
        // 数据库连接
        connectToDatabase();
        
        // 网络请求
        fetchDataFromAPI();
        
        // 文件操作
        loadConfiguration();
        
        // 数据处理
        processInitialData();
        
        // 缓存预热
        warmupCache();
        
        // 日志记录
        logInitialization();
    }
    
    // 违反接口隔离原则：一个接口包含太多不相关的方法
    void connectToDatabase() {
        std::cout << "Connecting to database..." << std::endl;
        // 硬编码的数据库连接
        if (name == "test") {
            isValid = true;
        }
    }
    
    void fetchDataFromAPI() {
        std::cout << "Fetching data from API..." << std::endl;
        // 网络操作与业务逻辑混合
        for (int i = 0; i < 100; i++) {
            data.push_back(i * 2);
        }
    }
    
    void loadConfiguration() {
        std::cout << "Loading configuration..." << std::endl;
        // 配置管理应该独立
    }
    
    void processInitialData() {
        // 复杂的嵌套循环，违反可读性原则
        for (size_t i = 0; i < data.size(); i++) {
            for (size_t j = i + 1; j < data.size(); j++) {
                for (size_t k = j + 1; k < data.size(); k++) {
                    if (data[i] + data[j] == data[k]) {
                        cache[std::to_string(i)] = data[i] * 1.5;
                        if (data[i] % 2 == 0) {
                            for (int l = 0; l < 10; l++) {
                                if (data[j] > data[k]) {
                                    errorCode += (data[i] / (data[j] - data[k] + 1));
                                } else {
                                    errorCode -= data[k];
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    void warmupCache() {
        std::cout << "Warming up cache..." << std::endl;
        // 缓存逻辑应该独立
    }
    
    void logInitialization() {
        std::cout << "Logging initialization..." << std::endl;
        // 日志记录应该独立
    }
    
    // 过长的方法，违反函数应该简短的原则
    std::string generateComplexReport() {
        std::string report = "=== COMPLEX REPORT ===\n";
        
        // 数据统计部分
        report += "Data Statistics:\n";
        double sum = 0, max = data[0], min = data[0];
        for (size_t i = 0; i < data.size(); i++) {
            sum += data[i];
            if (data[i] > max) max = data[i];
            if (data[i] < min) min = data[i];
        }
        double avg = sum / data.size();
        report += "Sum: " + std::to_string(sum) + "\n";
        report += "Average: " + std::to_string(avg) + "\n";
        report += "Max: " + std::to_string(max) + "\n";
        report += "Min: " + std::to_string(min) + "\n";
        
        // 缓存统计部分
        report += "\nCache Statistics:\n";
        report += "Cache size: " + std::to_string(cache.size()) + "\n";
        double cacheSum = 0;
        for (const auto& pair : cache) {
            cacheSum += pair.second;
        }
        report += "Cache sum: " + std::to_string(cacheSum) + "\n";
        
        // 错误分析部分
        report += "\nError Analysis:\n";
        if (errorCode > 0) {
            report += "Positive error code: " + std::to_string(errorCode) + "\n";
            if (errorCode > 100) {
                report += "High error level detected\n";
                if (errorCode > 500) {
                    report += "Critical error level!\n";
                    // 嵌套的错误处理逻辑
                    for (int i = 0; i < errorCode / 100; i++) {
                        report += "Error iteration " + std::to_string(i) + "\n";
                        if (i % 10 == 0) {
                            report += "Checkpoint reached\n";
                        }
                    }
                }
            }
        } else if (errorCode < 0) {
            report += "Negative error code: " + std::to_string(errorCode) + "\n";
        } else {
            report += "No errors detected\n";
        }
        
        // 验证部分
        report += "\nValidation:\n";
        if (isValid) {
            report += "Object is valid\n";
            // 复杂的验证逻辑
            bool allDataPositive = true;
            for (size_t i = 0; i < data.size(); i++) {
                if (data[i] < 0) {
                    allDataPositive = false;
                    break;
                }
            }
            if (allDataPositive) {
                report += "All data values are positive\n";
            } else {
                report += "Some data values are negative\n";
            }
        } else {
            report += "Object is invalid\n";
        }
        
        return report;
    }
    
    // 违反封装原则：暴露内部细节
    std::vector<int>& getDataReference() {
        return data;  // 返回内部数据的引用，破坏封装
    }
    
    std::map<std::string, double>& getCacheReference() {
        return cache;  // 同样破坏封装
    }
    
    // 参数过多的方法
    void updateData(int index, int newValue, bool validateRange, 
                   bool updateCache, bool logChange, bool checkBounds,
                   double multiplier, std::string reason, int priority,
                   bool asyncUpdate) {
        
        if (checkBounds && (index < 0 || index >= static_cast<int>(data.size()))) {
            std::cout << "Index out of bounds" << std::endl;
            return;
        }
        
        int oldValue = data[index];
        data[index] = static_cast<int>(newValue * multiplier);
        
        if (updateCache) {
            cache[std::to_string(index)] = newValue * 1.5;
        }
        
        if (logChange) {
            std::cout << "Changed value at " << index << " from " 
                     << oldValue << " to " << data[index] 
                     << " (reason: " << reason << ", priority: " << priority << ")" << std::endl;
        }
        
        if (validateRange) {
            // 复杂的验证逻辑
        }
        
        if (asyncUpdate) {
            // 异步更新逻辑
        }
    }
};

// 紧耦合的类设计
class DatabaseManager {
public:
    MegaClass* megaObject;  // 直接依赖具体类
    
    DatabaseManager(MegaClass* obj) : megaObject(obj) {}
    
    void saveData() {
        // 直接访问MegaClass的内部状态
        auto& data = megaObject->getDataReference();
        auto& cache = megaObject->getCacheReference();
        
        std::cout << "Saving " << data.size() << " data points and " 
                 << cache.size() << " cache entries" << std::endl;
    }
};

// 违反里式替换原则的继承
class BaseProcessor {
public:
    virtual void process() {
        std::cout << "Base processing" << std::endl;
    }
    
    virtual ~BaseProcessor() = default;
};

class SpecialProcessor : public BaseProcessor {
public:
    void process() override {
        throw std::runtime_error("Special processor cannot process!");  // 违反里式替换原则
    }
};

int main() {
    std::cout << "Starting complex architecture demo..." << std::endl;
    
    // 创建紧耦合的对象
    MegaClass mega("demo");
    DatabaseManager dbManager(&mega);
    
    // 复杂的操作调用
    std::string report = mega.generateComplexReport();
    std::cout << report << std::endl;
    
    // 破坏封装的操作
    auto& dataRef = mega.getDataReference();
    dataRef[0] = 999;  // 外部直接修改内部数据
    
    // 参数过多的方法调用
    mega.updateData(0, 42, true, true, true, true, 2.5, "testing", 1, false);
    
    // 保存数据
    dbManager.saveData();
    
    // 违反里式替换原则的示例
    std::vector<BaseProcessor*> processors;
    processors.push_back(new BaseProcessor());
    processors.push_back(new SpecialProcessor());
    
    for (auto* processor : processors) {
        try {
            processor->process();  // SpecialProcessor会抛出异常
        } catch (const std::exception& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
    }
    
    // 清理
    for (auto* processor : processors) {
        delete processor;
    }
    
    return 0;
}
