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
    
    // 潜在的死锁风险
    void transfer(BankAccount& other, double amount) {
        std::lock_guard<std::mutex> lock1(mtx);
        std::lock_guard<std::mutex> lock2(other.mtx);  // 可能死锁！
        
        if (balance >= amount) {
            balance -= amount;
            other.balance += amount;
        }
    }
    
    double get_balance() {
        return balance;  // 没有锁保护！
    }
};

// 全局共享变量，没有同步保护
int counter = 0;

void worker_thread() {
    for (int i = 0; i < 1000; ++i) {
        counter++;  // 竞态条件！
    }
}

int main() {
    std::vector<std::thread> threads;
    
    // 创建多个线程
    for (int i = 0; i < 4; ++i) {
        threads.emplace_back(worker_thread);
    }
    
    // 等待所有线程完成
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "Counter: " << counter << std::endl;  // 结果不确定
    
    return 0;
}
