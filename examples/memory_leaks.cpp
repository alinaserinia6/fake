/*
 * Example 2: Memory Management Issues
 * Includes memory leaks, dangling pointers, double free, etc.
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
        data = new int[n];  // Dynamic allocation
        backup = nullptr;
        
        // Forgot to initialise data
        // for (size_t i = 0; i < n; i++) {
        //     data[i] = 0;
        // }
    }
    
    ~DataProcessor() {
        delete[] data;  // Correctly freed
        // Forgot to check if backup needs to be freed
    }
    
    void processData() {
        // Memory leak: each call allocates new memory but does not free the old one
        if (backup != nullptr) {
            // Should free the old backup first, but forgot to do so
        }
        backup = new int[size];
        
        for (size_t i = 0; i < size; i++) {
            backup[i] = data[i] * 2;
        }
    }
    
    void dangerousOperation() {
        delete[] data;
        data = nullptr;
        
        // Dangling pointer: using already freed memory
        std::cout << "First element: " << data[0] << std::endl;
    }
    
    void doubleFree() {
        delete[] backup;
        backup = nullptr;
        delete[] backup;  // Double free, causes crash
    }
    
    int* getData() {
        return data;  // Returns internal pointer, may lead to external misuse
    }
    
    void unsafeAccess(size_t index) {
        // Out-of-bounds access: no boundary checking
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
        
        // If an exception occurs here, proc will never be freed
        if (size > 1000) {
            throw std::runtime_error("Size too large!");
        }
    }
    
    ~ResourceManager() {
        // Forgot to free the pointers in the vector
        // for (auto* proc : processors) {
        //     delete proc;
        // }
    }
};

void memoryLeakExample() {
    for (int i = 0; i < 100; i++) {
        int* temp = new int[1000];  // Allocate memory
        // Forgot to free: delete[] temp;
        
        // Local pointer lost, memory leak
    }
}

int main() {
    DataProcessor processor(10);
    
    // Normal processing
    processor.processData();
    processor.processData();  // Second call will leak the first backup
    
    // Get data pointer
    int* dataPtr = processor.getData();
    
    // Dangerous operation
    try {
        processor.dangerousOperation();  // Dangling pointer access
    } catch (...) {
        std::cout << "Crashed as expected" << std::endl;
    }
    
    // Out-of-bounds access
    processor.unsafeAccess(999);  // Far beyond array bounds
    
    // Memory leak example
    memoryLeakExample();
    
    // Resource management issue
    ResourceManager manager;
    try {
        manager.addProcessor(2000);  // Will throw an exception, causing memory leak
    } catch (const std::exception& e) {
        std::cout << "Exception: " << e.what() << std::endl;
    }
    
    return 0;
    // At program termination, a large amount of memory is not properly freed
}
