/*
Example C code file - contains some common security issues for testing
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Buffer overflow risk
void unsafe_copy(char* source) {
    char buffer[100];
    strcpy(buffer, source);  // Potential buffer overflow
    printf("Copied: %s\n", buffer);
}

// Memory leak risk
void memory_leak_example() {
    char* ptr = malloc(1000);
    if (ptr == NULL) {
        return;  // Memory not freed
    }
    // Forgot to call free(ptr)
}

// Null pointer dereference risk
void null_pointer_risk(int* data) {
    *data = 42;  // No check for NULL pointer
}

// Complex nested structure
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
    null_pointer_risk(null_ptr);  // This will cause a segmentation fault
    
    complex_function(10, 10, 50);
    
    return 0;
}
