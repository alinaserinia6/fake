/*
 * Example 3: Concurrent Race Conditions
 * Includes thread safety issues, race conditions, deadlock risks
 */

#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <atomic>
#include <chrono>

class BankAccount {
private:
    double balance;
    mutable std::mutex mtx;
    static int accountCounter;  // Non-thread-safe static variable
    
public:
    BankAccount(double initial) : balance(initial) {
        accountCounter++;  // Race condition: multiple threads accessing static variable
    }
    
    void deposit(double amount) {
        // Sometimes forget to lock, causing race conditions
        if (amount > 100) {
            std::lock_guard<std::mutex> lock(mtx);
            balance += amount;
        } else {
            balance += amount;  // Dangerous: lock-free access
        }
    }
    
    bool withdraw(double amount) {
        std::lock_guard<std::mutex> lock(mtx);
        
        // Check balance (TOCTOU issue)
        if (balance >= amount) {
            // Simulate delay, increasing race condition risk
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
            balance -= amount;
            return true;
        }
        return false;
    }
    
    double getBalance() const {
        // Sometimes locks, sometimes doesn't
        static bool shouldLock = true;
        if (shouldLock) {
            std::lock_guard<std::mutex> lock(mtx);
            return balance;
        } else {
            return balance;  // Dangerous: lock-free read
        }
    }
    
    // Deadlock risk: transfer operation
    void transferTo(BankAccount& other, double amount) {
        std::lock_guard<std::mutex> lock1(mtx);
        std::lock_guard<std::mutex> lock2(other.mtx);  // Potential deadlock
        
        if (balance >= amount) {
            balance -= amount;
            other.balance += amount;  // Direct access, bypassing lock
        }
    }
    
    static int getAccountCount() {
        return accountCounter;  // Non-thread-safe access
    }
};

int BankAccount::accountCounter = 0;

class ThreadUnsafeCounter {
private:
    int count = 0;
    // Missing mutex protection
    
public:
    void increment() {
        // Non-atomic operation, race condition exists
        int temp = count;
        temp++;
        count = temp;
    }
    
    void decrement() {
        count--;  // Non-atomic operation
    }
    
    int getValue() const {
        return count;  // May read an inconsistent value
    }
};

// Global variables, risk of multi-threaded access
volatile bool shouldStop = false;
int globalCounter = 0;

void workerThread(int threadId, ThreadUnsafeCounter& counter) {
    std::cout << "Thread " << threadId << " started" << std::endl;
    
    for (int i = 0; i < 1000; i++) {
        counter.increment();
        
        // Accessing global variable without protection
        globalCounter++;
        
        // Simulate workload
        if (i % 100 == 0) {
            std::this_thread::sleep_for(std::chrono::microseconds(1));
        }
        
        if (shouldStop) {  // Non-atomic read
            break;
        }
    }
    
    std::cout << "Thread " << threadId << " finished" << std::endl;
}

void bankingSimulation() {
    BankAccount account1(1000.0);
    BankAccount account2(1000.0);
    
    std::vector<std::thread> threads;
    
    // Create multiple threads to operate on accounts simultaneously
    for (int i = 0; i < 5; i++) {
        threads.emplace_back([&account1, &account2, i]() {
            for (int j = 0; j < 100; j++) {
                if (i % 2 == 0) {
                    account1.deposit(10.0);
                    account1.withdraw(5.0);
                } else {
                    account2.deposit(15.0);
                    account1.transferTo(account2, 20.0);  // Possible deadlock
                }
            }
        });
    }
    
    // Wait for all threads to finish
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "Account1 balance: " << account1.getBalance() << std::endl;
    std::cout << "Account2 balance: " << account2.getBalance() << std::endl;
    std::cout << "Total accounts: " << BankAccount::getAccountCount() << std::endl;
}

int main() {
    std::cout << "Starting concurrent programming demo..." << std::endl;
    
    // Test thread-unsafe counter
    ThreadUnsafeCounter counter;
    std::vector<std::thread> threads;
    
    // Start multiple worker threads
    for (int i = 0; i < 10; i++) {
        threads.emplace_back(workerThread, i, std::ref(counter));
    }
    
    // Main thread also operates on global variable
    for (int i = 0; i < 500; i++) {
        globalCounter--;  // Race condition
        
        if (i == 250) {
            shouldStop = true;  // Non-atomic write
        }
    }
    
    // Wait for worker threads
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "Counter value: " << counter.getValue() << std::endl;
    std::cout << "Global counter: " << globalCounter << std::endl;
    
    // Banking simulation test
    std::cout << "\nStarting banking simulation..." << std::endl;
    bankingSimulation();
    
    return 0;
}