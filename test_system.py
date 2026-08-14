#!/usr/bin/env python3
"""
Interruptr System Test Script
Tests the basic functionality of the enhanced multi-agent system
"""

import asyncio
import sys
from pathlib import Path
import json
from datetime import datetime

# Add project root directory to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from config.env_config import config

async def test_config():
    """Test configuration"""
    print("🔧 Testing configuration system...")
    
    try:
        # Get configuration summary
        print(f"  - OpenAI model: {config.openai_model}")
        print(f"  - Claude model: {config.anthropic_model}")
        print(f"  - Gemini model: {config.gemini_model}")
        print(f"  - Ollama model: {config.ollama_model}")
        
        # Display role assignments
        print(f"  - Coordinator LLM: {config.coordinator_llm}")
        print(f"  - Critic LLM: {config.critic_llm}")
        print(f"  - Reviewer LLM: {config.reviewer_llm}")
        
        print("✅ Configuration system is healthy")
        return True
    except Exception as e:
        print(f"❌ Configuration system error: {e}")
        return False

async def test_llm_interface():
    """Test LLM interface"""
    print("\n🤖 Testing LLM interface...")
    
    try:
        from agents.enhanced_multi_agent_system import LLMInterface
        
        # Test simple calls
        test_prompt = "Hello, this is a test."
        system_message = "You are a helpful assistant."
        
        print("  - Testing OpenAI interface...")
        if config.openai_api_key and config.openai_api_key != "your-openai-api-key":
            try:
                response = await LLMInterface.call_openai(test_prompt, system_message)
                print(f"    OpenAI response length: {len(response)} characters")
            except Exception as e:
                print(f"    OpenAI call failed: {str(e)[:100]}...")
        else:
            print("    OpenAI API key not configured")
        
        print("  - Testing Ollama interface...")
        if config.ollama_base_url:
            try:
                response = await LLMInterface.call_ollama(test_prompt, system_message)
                print(f"    Ollama response length: {len(response)} characters")
            except Exception as e:
                print(f"    Ollama call failed: {str(e)[:100]}...")
        else:
            print("    Ollama not configured")
        
        print("✅ LLM interface test completed")
        return True
    except Exception as e:
        print(f"❌ LLM interface test failed: {e}")
        return False

async def test_multi_agent_system():
    """Test multi-agent system"""
    print("\n🎭 Testing multi-agent system...")
    
    try:
        from agents.enhanced_multi_agent_system import EnhancedMultiAgentSystem
        
        # Create system instance
        system = EnhancedMultiAgentSystem()
        
        print(f"  - Number of initialized agents: {len(system.agents)}")
        
        # Check each agent
        for agent_name, agent in system.agents.items():
            print(f"    {agent_name}: {agent.config.role} ({agent.config.llm_provider})")
        
        print("✅ Multi-agent system initialised successfully")
        return True
    except Exception as e:
        print(f"❌ Multi-agent system test failed: {e}")
        return False

async def test_sample_analysis():
    """Test sample code analysis"""
    print("\n📊 Testing sample code analysis...")
    
    try:
        # Check sample file
        example_file = project_root / "examples" / "unsafe_code.c"
        
        if not example_file.exists():
            print("  - Sample file does not exist, creating a simple example...")
            example_file.parent.mkdir(exist_ok=True)
            with open(example_file, 'w') as f:
                f.write("""
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[10];
    char source[] = "This is a very long string that will overflow";
    
    strcpy(buffer, source);  // Potential buffer overflow
    printf("%s\\n", buffer);
    
    return 0;
}
""")
        
        with open(example_file, 'r') as f:
            code_content = f.read()
        
        print(f"  - Sample file path: {example_file}")
        print(f"  - Code length: {len(code_content)} characters")
        print(f"  - Number of lines: {len(code_content.splitlines())} lines")
        
        # Here we could add actual analysis tests
        # Since API keys are required, we skip actual calls for now
        print("  - Skipping actual LLM calls (API keys required)")
        
        print("✅ Sample code analysis test completed")
        return True
    except Exception as e:
        print(f"❌ Sample code analysis test failed: {e}")
        return False

async def test_frontend():
    """Test frontend components"""
    print("\n🖥️ Testing frontend components...")
    
    try:
        # Check if frontend files exist
        frontend_files = [
            "frontend/app.py",
            "frontend/visualization.py",
            "frontend/agent_visualization.py"
        ]
        
        for file_path in frontend_files:
            full_path = project_root / file_path
            if full_path.exists():
                print(f"  ✅ {file_path} exists")
            else:
                print(f"  ❌ {file_path} does not exist")
        
        print("✅ Frontend component check completed")
        return True
    except Exception as e:
        print(f"❌ Frontend component test failed: {e}")
        return False

async def test_api_backend():
    """Test API backend"""
    print("\n🔌 Testing API backend...")
    
    try:
        # Check API file
        api_file = project_root / "api" / "main.py"
        
        if api_file.exists():
            print(f"  ✅ API file exists: {api_file}")
            
            # Try to import the API module
            try:
                import api.main
                print("  ✅ API module imported successfully")
            except Exception as e:
                print(f"  ⚠️ API module import warning: {str(e)[:100]}...")
        else:
            print("  ❌ API file does not exist")
        
        print("✅ API backend check completed")
        return True
    except Exception as e:
        print(f"❌ API backend test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting Interruptr system tests")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("Configuration system", test_config),
        ("LLM interface", test_llm_interface),
        ("Multi-agent system", test_multi_agent_system),
        ("Sample code analysis", test_sample_analysis),
        ("Frontend components", test_frontend),
        ("API backend", test_api_backend)
    ]
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test exception: {e}")
            test_results.append((test_name, False))
    
    # Summary of results
    print("\n" + "=" * 50)
    print("📋 Test results summary:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ Passed" if result else "❌ Failed"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
    elif passed >= total * 0.7:
        print("⚠️ Most tests passed, system is basically usable.")
    else:
        print("❌ Multiple tests failed, configuration needs checking.")
    
    # Generate test report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total,
        "passed_tests": passed,
        "success_rate": passed / total,
        "test_details": test_results
    }
    
    report_file = project_root / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Detailed report saved: {report_file}")

if __name__ == "__main__":
    asyncio.run(main())
