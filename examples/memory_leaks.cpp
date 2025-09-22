/*
 * 示例2: 内存管理问题
 * 包含内存泄漏、野指针、重复释放等问题
 */

#include <iostream>
#include <vector>
#include <memory>

class DataProcessor {
private:
    int* data;
    size_t size;
    int* backup;
    
public:
    DataProcessor(size_t n) : size(n) {
        data = new int[n];  // 动态分配
        backup = nullptr;
        
        // 忘记初始化数据
        // for (size_t i = 0; i < n; i++) {
        //     data[i] = 0;
        // }
    }
    
    ~DataProcessor() {
        delete[] data;  // 正确释放
        // 忘记检查backup是否需要释放
    }
    
    void processData() {
        // 内存泄漏：每次调用都分配新内存但不释放旧的
        if (backup != nullptr) {
            // 应该先释放旧的backup，但忘记了
        }
        backup = new int[size];
        
        for (size_t i = 0; i < size; i++) {
            backup[i] = data[i] * 2;
        }
    }
    
    void dangerousOperation() {
        delete[] data;
        data = nullptr;
        
        // 野指针：使用已释放的内存
        std::cout << "First element: " << data[0] << std::endl;
    }
    
    void doubleFree() {
        delete[] backup;
        backup = nullptr;
        delete[] backup;  // 重复释放，导致崩溃
    }
    
    int* getData() {
        return data;  // 返回内部指针，可能导致外部误用
    }
    
    void unsafeAccess(size_t index) {
        // 数组越界：没有边界检查
        data[index] = 42;
    }
};

class ResourceManager {
private:
    std::vector<DataProcessor*> processors;
    
public:
    void addProcessor(size_t size) {
        DataProcessor* proc = new DataProcessor(size);
        processors.push_back(proc);
        
        // 如果这里发生异常，proc永远不会被释放
        if (size > 1000) {
            throw std::runtime_error("Size too large!");
        }
    }
    
    ~ResourceManager() {
        // 忘记释放vector中的指针
        // for (auto* proc : processors) {
        //     delete proc;
        // }
    }
};

void memoryLeakExample() {
    for (int i = 0; i < 100; i++) {
        int* temp = new int[1000];  // 分配内存
        // 忘记释放：delete[] temp;
        
        // 局部指针丢失，内存泄漏
    }
}

int main() {
    DataProcessor processor(10);
    
    // 正常处理
    processor.processData();
    processor.processData();  // 第二次调用会泄漏第一次的backup
    
    // 获取数据指针
    int* dataPtr = processor.getData();
    
    // 危险操作
    try {
        processor.dangerousOperation();  // 野指针访问
    } catch (...) {
        std::cout << "Crashed as expected" << std::endl;
    }
    
    // 数组越界
    processor.unsafeAccess(999);  // 远超数组边界
    
    // 内存泄漏示例
    memoryLeakExample();
    
    // 资源管理问题
    ResourceManager manager;
    try {
        manager.addProcessor(2000);  // 会抛出异常，导致内存泄漏
    } catch (const std::exception& e) {
        std::cout << "Exception: " << e.what() << std::endl;
    }
    
    return 0;
    // 程序结束时，大量内存没有正确释放
}
