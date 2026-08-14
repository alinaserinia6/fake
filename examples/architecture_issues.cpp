/*
 * Example 4: Complex Architecture Issues
 * Includes design pattern misuse, high coupling, unclear responsibilities, etc.
 */

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>

// Giant class that violates the Single Responsibility Principle
class MegaClass {
private:
    std::string name;
    std::vector<int> data;
    std::map<std::string, double> cache;
    bool isValid;
    int errorCode;
    
public:
    // Constructor does too many things
    MegaClass(const std::string& n) : name(n), isValid(false), errorCode(0) {
        // Database connection
        connectToDatabase();
        
        // Network request
        fetchDataFromAPI();
        
        // File operations
        loadConfiguration();
        
        // Data processing
        processInitialData();
        
        // Cache warmup
        warmupCache();
        
        // Logging
        logInitialization();
    }
    
    // Violates Interface Segregation Principle: one interface contains too many unrelated methods
    void connectToDatabase() {
        std::cout << "Connecting to database..." << std::endl;
        // Hard-coded database connection
        if (name == "test") {
            isValid = true;
        }
    }
    
    void fetchDataFromAPI() {
        std::cout << "Fetching data from API..." << std::endl;
        // Network operations mixed with business logic
        for (int i = 0; i < 100; i++) {
            data.push_back(i * 2);
        }
    }
    
    void loadConfiguration() {
        std::cout << "Loading configuration..." << std::endl;
        // Configuration management should be independent
    }
    
    void processInitialData() {
        // Complex nested loops, violating readability principles
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
        // Cache logic should be independent
    }
    
    void logInitialization() {
        std::cout << "Logging initialization..." << std::endl;
        // Logging should be independent
    }
    
    // Overly long method, violating the principle that functions should be short
    std::string generateComplexReport() {
        std::string report = "=== COMPLEX REPORT ===\n";
        
        // Data statistics section
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
        
        // Cache statistics section
        report += "\nCache Statistics:\n";
        report += "Cache size: " + std::to_string(cache.size()) + "\n";
        double cacheSum = 0;
        for (const auto& pair : cache) {
            cacheSum += pair.second;
        }
        report += "Cache sum: " + std::to_string(cacheSum) + "\n";
        
        // Error analysis section
        report += "\nError Analysis:\n";
        if (errorCode > 0) {
            report += "Positive error code: " + std::to_string(errorCode) + "\n";
            if (errorCode > 100) {
                report += "High error level detected\n";
                if (errorCode > 500) {
                    report += "Critical error level!\n";
                    // Nested error handling logic
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
        
        // Validation section
        report += "\nValidation:\n";
        if (isValid) {
            report += "Object is valid\n";
            // Complex validation logic
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
    
    // Violates encapsulation: exposes internal details
    std::vector<int>& getDataReference() {
        return data;  // Returns reference to internal data, breaking encapsulation
    }
    
    std::map<std::string, double>& getCacheReference() {
        return cache;  // Also breaks encapsulation
    }
    
    // Method with too many parameters
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
            // Complex validation logic
        }
        
        if (asyncUpdate) {
            // Asynchronous update logic
        }
    }
};

// Tightly coupled class design
class DatabaseManager {
public:
    MegaClass* megaObject;  // Direct dependency on concrete class
    
    DatabaseManager(MegaClass* obj) : megaObject(obj) {}
    
    void saveData() {
        // Direct access to MegaClass's internal state
        auto& data = megaObject->getDataReference();
        auto& cache = megaObject->getCacheReference();
        
        std::cout << "Saving " << data.size() << " data points and " 
                 << cache.size() << " cache entries" << std::endl;
    }
};

// Violates the Liskov Substitution Principle
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
        throw std::runtime_error("Special processor cannot process!");  // Violates Liskov Substitution Principle
    }
};

int main() {
    std::cout << "Starting complex architecture demo..." << std::endl;
    
    // Create tightly coupled objects
    MegaClass mega("demo");
    DatabaseManager dbManager(&mega);
    
    // Complex operation calls
    std::string report = mega.generateComplexReport();
    std::cout << report << std::endl;
    
    // Operation that breaks encapsulation
    auto& dataRef = mega.getDataReference();
    dataRef[0] = 999;  // External direct modification of internal data
    
    // Method call with too many parameters
    mega.updateData(0, 42, true, true, true, true, 2.5, "testing", 1, false);
    
    // Save data
    dbManager.saveData();
    
    // Example of violating the Liskov Substitution Principle
    std::vector<BaseProcessor*> processors;
    processors.push_back(new BaseProcessor());
    processors.push_back(new SpecialProcessor());
    
    for (auto* processor : processors) {
        try {
            processor->process();  // SpecialProcessor will throw an exception
        } catch (const std::exception& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
    }
    
    // Cleanup
    for (auto* processor : processors) {
        delete processor;
    }
    
    return 0;
}
