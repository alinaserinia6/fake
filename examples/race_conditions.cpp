/*
 * 示例3: 并发竞态条件
 * 包含线程安全问题、竞态条件、死锁风险
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
    static int accountCounter;  // 非线程安全的静态变量
    
public:
    BankAccount(double initial) : balance(initial) {
        accountCounter++;  // 竞态条件：多线程访问静态变量
    }
    
    void deposit(double amount) {
        // 有时忘记加锁，导致竞态条件
        if (amount > 100) {
            std::lock_guard<std::mutex> lock(mtx);
            balance += amount;
        } else {
            balance += amount;  // 危险：无锁访问
        }
    }
    
    bool withdraw(double amount) {
        std::lock_guard<std::mutex> lock(mtx);
        
        // 检查余额（TOCTOU问题）
        if (balance >= amount) {
            // 模拟延迟，增加竞态条件风险
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
            balance -= amount;
            return true;
        }
        return false;
    }
    
    double getBalance() const {
        // 有时加锁，有时不加锁
        static bool shouldLock = true;
        if (shouldLock) {
            std::lock_guard<std::mutex> lock(mtx);
            return balance;
        } else {
            return balance;  // 危险：无锁读取
        }
    }
    
    // 死锁风险：transfer操作
    void transferTo(BankAccount& other, double amount) {
        std::lock_guard<std::mutex> lock1(mtx);
        std::lock_guard<std::mutex> lock2(other.mtx);  // 可能死锁
        
        if (balance >= amount) {
            balance -= amount;
            other.balance += amount;  // 直接访问，绕过锁
        }
    }
    
    static int getAccountCount() {
        return accountCounter;  // 非线程安全访问
    }
};

int BankAccount::accountCounter = 0;

class ThreadUnsafeCounter {
private:
    int count = 0;
    // 缺少互斥锁保护
    
public:
    void increment() {
        // 非原子操作，存在竞态条件
        int temp = count;
        temp++;
        count = temp;
    }
    
    void decrement() {
        count--;  // 非原子操作
    }
    
    int getValue() const {
        return count;  // 可能读到不一致的值
    }
};

// 全局变量，多线程访问风险
volatile bool shouldStop = false;
int globalCounter = 0;

void workerThread(int threadId, ThreadUnsafeCounter& counter) {
    std::cout << "Thread " << threadId << " started" << std::endl;
    
    for (int i = 0; i < 1000; i++) {
        counter.increment();
        
        // 访问全局变量无保护
        globalCounter++;
        
        // 模拟工作负载
        if (i % 100 == 0) {
            std::this_thread::sleep_for(std::chrono::microseconds(1));
        }
        
        if (shouldStop) {  // 非原子读取
            break;
        }
    }
    
    std::cout << "Thread " << threadId << " finished" << std::endl;
}

void bankingSimulation() {
    BankAccount account1(1000.0);
    BankAccount account2(1000.0);
    
    std::vector<std::thread> threads;
    
    // 创建多个线程同时操作账户
    for (int i = 0; i < 5; i++) {
        threads.emplace_back([&account1, &account2, i]() {
            for (int j = 0; j < 100; j++) {
                if (i % 2 == 0) {
                    account1.deposit(10.0);
                    account1.withdraw(5.0);
                } else {
                    account2.deposit(15.0);
                    account1.transferTo(account2, 20.0);  // 可能死锁
                }
            }
        });
    }
    
    // 等待所有线程完成
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "Account1 balance: " << account1.getBalance() << std::endl;
    std::cout << "Account2 balance: " << account2.getBalance() << std::endl;
    std::cout << "Total accounts: " << BankAccount::getAccountCount() << std::endl;
}

int main() {
    std::cout << "Starting concurrent programming demo..." << std::endl;
    
    // 测试线程不安全的计数器
    ThreadUnsafeCounter counter;
    std::vector<std::thread> threads;
    
    // 启动多个工作线程
    for (int i = 0; i < 10; i++) {
        threads.emplace_back(workerThread, i, std::ref(counter));
    }
    
    // 主线程也操作全局变量
    for (int i = 0; i < 500; i++) {
        globalCounter--;  // 竞态条件
        
        if (i == 250) {
            shouldStop = true;  // 非原子写入
        }
    }
    
    // 等待工作线程
    for (auto& t : threads) {
        t.join();
    }
    
    std::cout << "Counter value: " << counter.getValue() << std::endl;
    std::cout << "Global counter: " << globalCounter << std::endl;
    
    // 银行模拟测试
    std::cout << "\nStarting banking simulation..." << std::endl;
    bankingSimulation();
    
    return 0;
}
