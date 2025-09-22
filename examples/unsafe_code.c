/*
示例C代码文件 - 包含一些常见的安全问题用于测试
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// 缓冲区溢出风险
void unsafe_copy(char* source) {
    char buffer[100];
    strcpy(buffer, source);  // 潜在缓冲区溢出
    printf("Copied: %s\n", buffer);
}

// 内存泄漏风险
void memory_leak_example() {
    char* ptr = malloc(1000);
    if (ptr == NULL) {
        return;  // 没有释放内存
    }
    // 忘记调用 free(ptr)
}

// 空指针解引用风险
void null_pointer_risk(int* data) {
    *data = 42;  // 没有检查指针是否为NULL
}

// 复杂的嵌套结构
void complex_function(int x, int y, int z) {
    if (x > 0) {
        if (y > 0) {
            if (z > 0) {
                for (int i = 0; i < x; i++) {
                    for (int j = 0; j < y; j++) {
                        if (i * j > z) {
                            printf("Result: %d\n", i * j);
                        }
                    }
                }
            }
        }
    }
}

int main() {
    char large_input[1000];
    strcpy(large_input, "This could cause buffer overflow if too long");
    
    unsafe_copy(large_input);
    memory_leak_example();
    
    int* null_ptr = NULL;
    null_pointer_risk(null_ptr);  // 这会导致段错误
    
    complex_function(10, 10, 50);
    
    return 0;
}
