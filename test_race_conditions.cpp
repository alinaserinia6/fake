#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <atomic>

class BankAccount {
private:
    double balance;
    std::mutex mtx;
    
public:
    BankAccount(double initial) : balance(initial) {}
    
    // Potential deadlock risk
    void transfer(BankAccount& other, double amount) {
        std::lock_guard<std::mutex> lock1(mtx);
        std::lock_guard<std::mutex> lock2(other.mtx);  // Possible deadlock!
        
        if (balance >= amount) {
            balance -= amount;
            other.balance += amount;
        }
    }
    
    double get_balance() {
        return balance;  // No lock protection!
    }
};

// Global shared variable, no synchronisation protection
int counter = 0;

void worker_thread() {
    for (int i = 0; i < 1000; ++i) {
        counter++;  // Race condition!
    }
}

int main() {
    std::vector<std::thread> threads;
    
    // Create multiple threads
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back(worker_thread);
    }
    
    // Wait for all threads to complete
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "Counter: " << counter << std::endl;  // Result is indeterminate
    
    return 0;
}