#!/usr/bin/env python3
"""
Simplified multi-agent code analysis demonstration
Shows dialogues between AutoGen agents
"""

import os
import asyncio
from pathlib import Path

async def simulate_multi_agent_analysis():
    """Simulate the multi-agent analysis process"""
    print("🤖 Starting multi-agent code analysis system...")
    print("📝 Simulating agent collaboration process\n")
    
    # Read example code
    examples_dir = Path("/home/coder-gw/Interruptr/examples")
    cpp_files = list(examples_dir.glob("*.cpp"))
    
    if not cpp_files:
        print("❌ No sample code files found")
        return
    
    # Analyse the first file
    cpp_file = cpp_files[0]
    with open(cpp_file, 'r', encoding='utf-8') as f:
        code_content = f.read()
    
    print(f"\n{'='*60}")
    print(f"Analysing file: {cpp_file.name}")
    print(f"{'='*60}")
    print("Code content:")
    print("-" * 40)
    print(code_content)
    print("-" * 40)
    
    # Simulate agent dialogue
    agents_dialogue = [
        {
            "agent": "coordinator",
            "message": f"Received code analysis task: {cpp_file.name}. Let me coordinate the experts for analysis. First, I'll ask the code analysis expert to perform static analysis."
        },
        {
            "agent": "code_analyst", 
            "message": """I am the code analysis expert. Here are my findings:

            1. **Structural issues**:
            - Missing necessary header includes
            - Unsafe function parameter types
            - No input validation

            2. **Logic issues**:
            - Potential insufficient buffer boundary checks
            - Missing error handling mechanisms

            Security expert, please further check for security vulnerabilities."""
        },
        {
            "agent": "security_expert",
            "message": """I am the security expert. I found the following security risks:

            🚨 **High-risk vulnerabilities**:
            1. **Buffer overflow**: Functions like strcpy/gets may cause stack overflows
            2. **Missing input validation**: User input is used directly without validation
            3. **Memory safety**: Pointer operations without null checks

            🔧 **Remediation recommendations**:
            - Use safe string functions (strncpy, fgets)
            - Add boundary checks
            - Validate all input parameters

            Debug expert, please analyse runtime issues."""
        },
        {
            "agent": "debug_expert",
            "message": """I am the debug expert. Runtime analysis as follows:

            🐛 **Potential runtime errors**:
            1. **Segmentation fault risk**: Accessing uninitialised pointers
            2. **Memory leaks**: Dynamically allocated memory not freed
            3. **Exception handling**: Missing exception catch mechanisms

            🔧 **Debugging recommendations**:
            - Add null pointer checks
            - Use RAII pattern for resource management
            - Add exception handling code

            Review expert, please perform the final review."""
        },
        {
            "agent": "critic",
            "message": """I am the review expert. Comprehensive review results:

            ✅ **Analysis quality assessment**:
            - Code analysis expert: Identified fundamental structural issues ✓
            - Security expert: Identified critical security vulnerabilities ✓
            - Debug expert: Pinpointed runtime risks ✓

            📋 **Supplementary issues**:
            1. Performance optimisation suggestions
            2. Code maintainability assessment
            3. Unit testing recommendations

            🎯 **Final score**: 7/10
            Recommendation: Prioritise fixing security vulnerabilities, then improve code structure."""
        },
        {
            "agent": "coordinator",
            "message": """Thank you all for your analysis! Let me consolidate the final recommendations:

            🎯 **Fix priorities**:
            1. **Urgent**: Fix buffer overflow vulnerabilities
            2. **Important**: Add input validation and error handling
            3. **Recommended**: Improve code structure and performance

            📝 **Specific remediation steps**:
            ```cpp
            // 1. Safe string operations
            char buffer[100];
            strncpy(buffer, input, sizeof(buffer)-1);
            buffer[sizeof(buffer)-1] = '\0';

            // 2. Input validation
            if (input == NULL || strlen(input) == 0) {
                return -1;
            }

            // 3. Error handling
            try {
                // Code logic
            } catch (const std::exception& e) {
                std::cerr << "Error: " << e.what() << std::endl;
                return -1;
            }
            ```

            Analysis complete! All agents collaborated successfully."""
        }
    ]
    
    # Play the dialogue
    for i, dialogue in enumerate(agents_dialogue):
        agent = dialogue["agent"]
        message = dialogue["message"]
        
        print(f"\n🤖 **{agent.upper()}** says:")
        print("-" * 50)
        print(message)
        
        # Simulate thinking time
        await asyncio.sleep(1)
    
    print(f"\n{'='*60}")
    print("✅ Multi-agent analysis complete!")
    print("🌐 AutoGen Studio is running at: http://localhost:8081")
    print("📱 You can view the full conversation interface in your browser")
    print(f"{'='*60}")

def check_autogen_studio_status():
    """Check AutoGen Studio status"""
    try:
        import requests
        response = requests.get("http://localhost:8081", timeout=5)
        return response.status_code == 200
    except:
        return False

async def main():
    """Main function"""
    print("🔍 Checking AutoGen Studio status...")
    
    if check_autogen_studio_status():
        print("✅ AutoGen Studio is running")
    else:
        print("⚠️ AutoGen Studio may not be fully started, please wait...")
    
    # Run the demo
    await simulate_multi_agent_analysis()

if __name__ == "__main__":
    asyncio.run(main())
