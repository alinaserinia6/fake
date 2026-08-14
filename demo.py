#!/usr/bin/env python3
"""
Interruptr Multi-Agent Demonstration Script
Test agent analysis capabilities with actual C++ defective code
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root directory to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from agents.enhanced_multi_agent_system import EnhancedMultiAgentSystem
from config.env_config import config

class DemoRunner:
    """Demo runner"""
    
    def __init__(self):
        self.test_files = [
            {
                "name": "buffer_overflow.cpp",
                "description": "Buffer overflow vulnerability example",
                "focus": "Security vulnerability detection"
            },
            {
                "name": "memory_leaks.cpp", 
                "description": "Memory management problem example",
                "focus": "Memory safety analysis"
            },
            {
                "name": "race_conditions.cpp",
                "description": "Concurrency race condition example",
                "focus": "Thread safety analysis"
            },
            {
                "name": "architecture_issues.cpp",
                "description": "Architecture design problem example",
                "focus": "Architecture quality assessment"
            }
        ]
        
        self.results = {}
    
    def display_banner(self):
        """Display demo banner"""
        print("🎭" + "="*70 + "🎭")
        print("🚀 Interruptr Multi-Agent C++ Code Analysis Demo")
        print("💡 7 specialized agents collaborate to analyze C++ code defects")
        print("🤖 Using OpenAI + Claude + Gemini + Ollama")
        print("="*72)
        
    def display_test_files(self):
        """Display test file information"""
        print("\n📁 Test file overview:")
        print("-" * 50)
        
        for i, file_info in enumerate(self.test_files, 1):
            file_path = project_root / "examples" / file_info["name"]
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                lines = len(content.splitlines())
                chars = len(content)
                
                print(f"{i}. {file_info['name']}")
                print(f"   📄 {file_info['description']}")
                print(f"   🎯 Analysis focus: {file_info['focus']}")
                print(f"   📊 Code stats: {lines} lines, {chars} characters")
                print()
            else:
                print(f"❌ {file_info['name']} file does not exist")
    
    def check_llm_availability(self):
        """Check LLM availability"""
        print("🔍 Checking LLM provider configuration:")
        print("-" * 40)
        
        providers = [
            ("OpenAI", config.openai_api_key, "Coordinator + Debug Expert"),
            ("Claude", config.anthropic_api_key, "Code Analyst + Security Expert + Architect"),
            ("Gemini", config.gemini_api_key, "Critic"),
            ("Ollama", config.ollama_base_url, "Reviewer")
        ]
        
        available_count = 0
        for name, key_or_url, roles in providers:
            if key_or_url and key_or_url != f"your-{name.lower()}-api-key":
                print(f"✅ {name}: Configured ({roles})")
                available_count += 1
            else:
                print(f"❌ {name}: Not configured")
        
        print(f"\n📊 LLM availability: {available_count}/4 providers configured")
        
        if available_count == 0:
            print("⚠️ Warning: No LLM providers configured; mock responses will be used")
            return False
        elif available_count < 4:
            print("⚠️ Hint: Some LLMs are not configured, analysis quality may be affected")
        else:
            print("🎉 All LLM providers configured, ready to start analysis")
        
        return available_count > 0
    
    async def analyze_single_file(self, file_info, use_real_llm=False):
        """Analyze a single file"""
        file_path = project_root / "examples" / file_info["name"]
        
        print(f"\n🔬 Starting analysis: {file_info['name']}")
        print(f"🎯 Analysis focus: {file_info['focus']}")
        print("=" * 60)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            if use_real_llm:
                # Use the real multi-agent system
                system = EnhancedMultiAgentSystem()
                result = await system.analyze_code_file(str(file_path), code_content)
                return result
            else:
                # Use mock analysis results
                return self.generate_mock_analysis(file_info, code_content)
                
        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")
            return None
    
    def generate_mock_analysis(self, file_info, code_content):
        """Generate mock analysis results"""
        print("🤖 Simulating multi-agent analysis process...")
        
        # Simulate the analysis process
        agents = [
            "🎯 Coordinator",
            "📊 Code Analyst", 
            "🔒 Security Expert",
            "🐛 Debug Expert",
            "🏛️ Architect",
            "🤔 Critic",
            "✅ Reviewer"
        ]
        
        for i, agent in enumerate(agents, 1):
            print(f"  [{i}/7] {agent} is analyzing...")
        
        # Generate specific analysis results based on file type
        if "buffer_overflow" in file_info["name"]:
            return self.generate_buffer_overflow_analysis()
        elif "memory_leaks" in file_info["name"]:
            return self.generate_memory_analysis()
        elif "race_conditions" in file_info["name"]:
            return self.generate_concurrency_analysis()
        elif "architecture" in file_info["name"]:
            return self.generate_architecture_analysis()
        else:
            return self.generate_generic_analysis()
    
    def generate_buffer_overflow_analysis(self):
        """Generate buffer overflow analysis results"""
        return {
            "status": "completed",
            "analysis_results": {
                "code_quality": {
                    "score": 3.2,
                    "issues": [
                        "Using deprecated dangerous function gets()",
                        "strcpy() function lacks boundary checking",
                        "scanf() misuse may cause buffer overflow",
                        "Missing input validation and boundary checks"
                    ]
                },
                "security": {
                    "critical_issues": [
                        {
                            "type": "Buffer overflow",
                            "line": 18,
                            "function": "setCredentials",
                            "description": "strcpy() can cause buffer overflow",
                            "severity": "High",
                            "cwe": "CWE-120"
                        },
                        {
                            "type": "Deprecated function",
                            "line": 31,
                            "function": "authenticate", 
                            "description": "gets() is deprecated and has serious security risks",
                            "severity": "Critical",
                            "cwe": "CWE-242"
                        }
                    ],
                    "recommendations": [
                        "Use strncpy() or strlcpy() instead of strcpy()",
                        "Use fgets() instead of gets()",
                        "Add input length validation",
                        "Use safe string handling functions"
                    ]
                },
                "debug": {
                    "breakpoints": [
                        "Line 18: Check parameter length before strcpy()",
                        "Line 31: Monitor gets() function call",
                        "Line 47: Validate input buffer size",
                        "Line 55: Check scanf() input length"
                    ]
                },
                "architecture": {
                    "issues": [
                        "UserManager class has too many responsibilities",
                        "Missing input validation layer",
                        "Hard-coded buffer sizes",
                        "Error handling mechanism is inadequate"
                    ]
                },
                "critic_review": "The security expert's analysis is mostly accurate, but we should also consider format string attacks. The printf() on line 24 uses user input as the format string, which is also a serious security vulnerability.",
                "final_review": "After validation, the code indeed contains multiple severe buffer overflow risks. It is recommended to fix these issues immediately and implement a code security review process."
            }
        }
    
    def generate_memory_analysis(self):
        """Generate memory management analysis results"""
        return {
            "status": "completed", 
            "analysis_results": {
                "code_quality": {
                    "score": 4.1,
                    "issues": [
                        "Potential memory leak",
                        "Dangling pointer access",
                        "Double free risk",
                        "Lack of RAII pattern usage"
                    ]
                },
                "security": {
                    "critical_issues": [
                        {
                            "type": "Memory leak",
                            "line": 32,
                            "function": "processData",
                            "description": "backup pointer reallocated without freeing old memory",
                            "severity": "Medium"
                        },
                        {
                            "type": "Dangling pointer access",
                            "line": 44,
                            "function": "dangerousOperation",
                            "description": "Using a pointer to already freed memory",
                            "severity": "High"
                        }
                    ]
                },
                "debug": {
                    "breakpoints": [
                        "Line 32: Check if backup pointer has been freed before reassignment",
                        "Line 44: Verify data pointer state",
                        "Line 150: Monitor ResourceManager destructor",
                        "Line 156: Check memory state during exception throwing"
                    ]
                },
                "architecture": {
                    "recommendations": [
                        "Use smart pointers (std::unique_ptr, std::shared_ptr)",
                        "Implement RAII pattern",
                        "Add exception safety guarantees",
                        "Use container classes instead of raw arrays"
                    ]
                },
                "critic_review": "The memory management analysis is relatively thorough, but should emphasise the importance of using modern C++ features. Consider using std::vector instead of raw arrays, and smart pointers to manage dynamic memory.",
                "final_review": "The code has multiple memory management issues and needs refactoring to use modern C++ memory management techniques."
            }
        }
    
    def generate_concurrency_analysis(self):
        """Generate concurrency analysis results"""
        return {
            "status": "completed",
            "analysis_results": {
                "code_quality": {
                    "score": 3.8,
                    "issues": [
                        "Race condition exists",
                        "Inconsistent mutex usage",
                        "Possible deadlock risk",
                        "Concurrent access to non-atomic operations"
                    ]
                },
                "security": {
                    "critical_issues": [
                        {
                            "type": "Race condition",
                            "line": 18,
                            "function": "BankAccount constructor",
                            "description": "Non-thread-safe access to static variable accountCounter",
                            "severity": "Medium"
                        },
                        {
                            "type": "Deadlock risk",
                            "line": 57,
                            "function": "transferTo",
                            "description": "Lock ordering of multiple mutexes may cause deadlock",
                            "severity": "High"
                        }
                    ]
                },
                "debug": {
                    "breakpoints": [
                        "Line 18: Monitor concurrent access to accountCounter",
                        "Line 26: Check lock state in deposit function", 
                        "Lines 57-58: Monitor lock acquisition order in transferTo",
                        "Line 98: Observe race condition in ThreadUnsafeCounter"
                    ]
                },
                "architecture": {
                    "recommendations": [
                        "Use std::atomic instead of volatile variables",
                        "Implement a consistent locking strategy",
                        "Consider lock-free data structures",
                        "Add thread-safe logging"
                    ]
                },
                "critic_review": "The concurrency analysis accurately identifies the main issues. Also consider using std::lock() to avoid deadlocks, and condition variables to improve thread synchronisation.",
                "final_review": "The code has serious thread-safety issues and needs a redesign of concurrency strategies and synchronisation mechanisms."
            }
        }
    
    def generate_architecture_analysis(self):
        """Generate architecture analysis results"""
        return {
            "status": "completed",
            "analysis_results": {
                "code_quality": {
                    "score": 2.5,
                    "issues": [
                        "Violates the Single Responsibility Principle",
                        "High coupling between classes",
                        "Excessively complex methods",
                        "Overly long parameter lists"
                    ]
                },
                "security": {
                    "critical_issues": [
                        {
                            "type": "Encapsulation breach",
                            "line": 142,
                            "function": "getDataReference",
                            "description": "Returns reference to internal data, breaking encapsulation",
                            "severity": "Medium"
                        }
                    ]
                },
                "debug": {
                    "breakpoints": [
                        "Line 25: Monitor complex initialisation in MegaClass constructor",
                        "Line 85: Check nested logic in generateComplexReport",
                        "Line 154: Observe parameter handling in updateData",
                        "Line 200: Monitor exception throwing in SpecialProcessor"
                    ]
                },
                "architecture": {
                    "violations": [
                        "Single Responsibility Principle: MegaClass takes on too many responsibilities",
                        "Open/Closed Principle: Class design is not easily extensible",
                        "Liskov Substitution Principle: SpecialProcessor violates base class contract",
                        "Interface Segregation Principle: Interface is too large",
                        "Dependency Inversion Principle: Direct dependency on concrete classes rather than abstractions"
                    ],
                    "recommendations": [
                        "Split MegaClass into multiple classes with clear responsibilities",
                        "Use Factory pattern to create objects",
                        "Introduce interface abstraction layers",
                        "Reduce method parameters, use configuration objects",
                        "Implement Dependency Injection pattern"
                    ]
                },
                "critic_review": "The architecture analysis is thorough and correctly identifies SOLID principle violations. Also consider using the Command pattern to handle complex operations, and the Strategy pattern for different processing strategies.",
                "final_review": "The code has serious architectural design issues and requires large-scale refactoring to improve maintainability and extensibility."
            }
        }
    
    def generate_generic_analysis(self):
        """Generate generic analysis results"""
        return {
            "status": "completed",
            "analysis_results": {
                "code_quality": {"score": 6.0, "issues": []},
                "security": {"critical_issues": []},
                "debug": {"breakpoints": []},
                "architecture": {"recommendations": []},
                "critic_review": "Code quality is acceptable.",
                "final_review": "No serious issues found."
            }
        }
    
    def display_analysis_summary(self, file_info, result):
        """Display analysis summary"""
        if not result:
            print("❌ Analysis failed")
            return
        
        analysis = result.get("analysis_results", {})
        
        print(f"\n📊 {file_info['name']} Analysis Summary:")
        print("-" * 50)
        
        # Code quality
        quality = analysis.get("code_quality", {})
        if isinstance(quality, dict):
            score = quality.get("score", 0)
            print(f"🎯 Code quality score: {score}/10.0")
        else:
            print(f"🎯 Code quality: {str(quality)[:50]}...")
        
        # Security issues
        security = analysis.get("security", {})
        if isinstance(security, dict):
            issues = security.get("critical_issues", [])
            print(f"🔒 Security issues: {len(issues)}")
            
            if issues:
                for issue in issues[:3]:  # Show first 3 issues
                    if isinstance(issue, dict):
                        print(f"   • {issue.get('type', 'Unknown')} (line {issue.get('line', '?')})")
                    else:
                        print(f"   • {str(issue)[:50]}...")
        else:
            print(f"🔒 Security analysis: {str(security)[:50]}...")
        
        # Critic review
        critic = analysis.get("critic_review", "")
        if critic:
            print(f"🤔 Critic: {str(critic)[:100]}...")
        
        # Final assessment
        final = analysis.get("final_review", "")
        if final:
            print(f"✅ Final assessment: {str(final)[:100]}...")
        
        print()
    
    def save_results(self):
        """Save demo results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = project_root / f"demo_results_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Demo results saved: {output_file}")
    
    async def run_demo(self):
        """Run the complete demo"""
        self.display_banner()
        self.display_test_files()
        
        use_real_llm = self.check_llm_availability()
        
        print(f"\n🚀 Starting multi-agent analysis demo ({'Real LLM' if use_real_llm else 'Mock mode'})")
        print("=" * 72)
        
        for i, file_info in enumerate(self.test_files, 1):
            print(f"\n[{i}/4] Analyzing file: {file_info['name']}")
            
            result = await self.analyze_single_file(file_info, use_real_llm)
            
            if result:
                self.results[file_info["name"]] = result
                self.display_analysis_summary(file_info, result)
            
            # Add interval
            if i < len(self.test_files):
                print("⏳ Preparing next analysis...")
                await asyncio.sleep(1)
        
        print("\n🎉 All files analysed!")
        self.save_results()
        
        # Display summary
        print("\n📈 Demo summary:")
        print("-" * 30)
        total_files = len(self.test_files)
        analyzed_files = len(self.results)
        print(f"• Total files: {total_files}")
        print(f"• Successfully analysed: {analyzed_files}")
        print(f"• Success rate: {analyzed_files/total_files*100:.1f}%")
        
        if use_real_llm:
            print("• Used real LLM APIs for analysis")
        else:
            print("• Used mock mode for demonstration")
        
        print(f"\n💡 Suggestions:")
        if not use_real_llm:
            print("• Configure real API keys to obtain more accurate analysis results")
        print("• Use 'python start.py' to start the web interface for interactive analysis")
        print("• Review the generated report files for detailed analysis results")

async def main():
    """Main function"""
    demo = DemoRunner()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())
