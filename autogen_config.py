"""
AutoGen Studio Configuration File - Multi-Agent Code Analysis System
"""
import os
from pathlib import Path

# AutoGen Studio Configuration
AUTOGEN_CONFIG = {
    "models": [
        {
            "model": "gpt-4",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": "https://api.openai.com/v1",
            "api_type": "openai",
            "model_name": "gpt-4"
        },
        {
            "model": "claude-3-sonnet",
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "base_url": "https://api.anthropic.com",
            "api_type": "anthropic",
            "model_name": "claude-3-sonnet-20240229"
        },
        {
            "model": "gpt-oss",
            "api_key": "ollama",
            "base_url": "http://localhost:11434/v1",
            "api_type": "ollama",
            "model_name": "gpt-oss:latest"
        }
    ],
    
    "agents": [
        {
            "name": "coordinator",
            "description": "Coordinator: responsible for task decomposition and process management",
            "system_message": """You are the coordinator of a multi-agent system.
Your tasks are:
1. Receive code analysis requests
2. Decompose complex tasks into subtasks
3. Coordinate the work of each expert agent
4. Consolidate analysis results
5. Provide final remediation recommendations

Always remain professional, accurate, and efficient.""",
            "model": "gpt-4",
            "max_consecutive_auto_reply": 10
        },
        {
            "name": "code_analyst",
            "description": "Code Analysis Expert: focuses on code structure and logic analysis",
            "system_message": """You are a professional code analysis expert.
Your areas of expertise include:
1. Static code analysis
2. Code structure assessment
3. Logical flow analysis
4. Code quality evaluation
5. Performance bottleneck identification

Provide detailed technical details and improvement suggestions in your analysis.""",
            "model": "claude-3-sonnet",
            "max_consecutive_auto_reply": 5
        },
        {
            "name": "security_expert",
            "description": "Security Expert: focuses on security vulnerability detection",
            "system_message": """You are a cybersecurity expert.
Your areas of expertise include:
1. Security vulnerability detection (buffer overflows, injection attacks, etc.)
2. Secure code auditing
3. Threat modeling
4. Security best practices
5. Vulnerability remediation suggestions

Provide detailed security analysis and remediation plans.""",
            "model": "gpt-4",
            "max_consecutive_auto_reply": 5
        },
        {
            "name": "debug_expert",
            "description": "Debug Expert: focuses on error localization and fixing",
            "system_message": """You are a debugging expert.
Your areas of expertise include:
1. Runtime error analysis
2. Memory leak detection
3. Deadlock and race condition analysis
4. Performance problem diagnosis
5. Error remediation plans

Provide precise error localization and feasible repair solutions.""",
            "model": "gpt-oss",
            "max_consecutive_auto_reply": 5
        },
        {
            "name": "architect",
            "description": "Architect: focuses on system design and refactoring suggestions",
            "system_message": """You are a software architect.
Your areas of expertise include:
1. System architecture design
2. Code refactoring suggestions
3. Design pattern application
4. Maintainability assessment
5. Scalability analysis

Provide system-level improvement suggestions.""",
            "model": "claude-3-sonnet",
            "max_consecutive_auto_reply": 5
        },
        {
            "name": "critic",
            "description": "Review Expert: responsible for quality control and final review",
            "system_message": """You are a code review expert.
Your responsibilities are:
1. Review the analysis results of other experts
2. Verify the feasibility of remediation plans
3. Provide quality assurance
4. Identify overlooked issues
5. Ensure completeness of the final solution

Provide objective and comprehensive review comments.""",
            "model": "gpt-4",
            "max_consecutive_auto_reply": 3
        }
    ],
    
    "workflows": [
        {
            "name": "c_cpp_code_analysis",
            "description": "C/C++ Code Analysis Workflow",
            "sender": "coordinator",
            "receiver": "code_analyst",
            "summary_method": "reflection_with_llm",
            "max_turns": 20,
            "participants": [
                "coordinator",
                "code_analyst", 
                "security_expert",
                "debug_expert",
                "architect",
                "critic"
            ]
        }
    ],
    
    "skills": [
        {
            "name": "cpp_static_analysis",
            "description": "C++ static code analysis",
            "content": """
def analyze_cpp_code(code_content, file_path):
    '''Analyze static issues in C++ code'''
    import subprocess
    import tempfile
    
    # Save code to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
        f.write(code_content)
        temp_file = f.name
    
    results = []
    
    # Compilation check
    try:
        result = subprocess.run(['g++', '-Wall', '-Wextra', '-fsyntax-only', temp_file],
                              capture_output=True, text=True)
        if result.stderr:
            results.append(f"Compilation warnings/errors:\\n{result.stderr}")
    except Exception as e:
        results.append(f"Compilation check failed: {e}")
    
    # cppcheck static analysis
    try:
        result = subprocess.run(['cppcheck', '--enable=all', '--verbose', temp_file],
                              capture_output=True, text=True)
        if result.stderr:
            results.append(f"cppcheck analysis:\\n{result.stderr}")
    except Exception as e:
        results.append(f"cppcheck analysis failed: {e}")
    
    # Clean up temporary file
    import os
    os.unlink(temp_file)
    
    return "\\n\\n".join(results) if results else "No obvious issues found"
"""
        }
    ]
}

def create_autogen_studio_config():
    """Create AutoGen Studio configuration file"""
    config_dir = Path.home() / ".autogenstudio" 
    config_dir.mkdir(exist_ok=True)
    
    # Write configuration
    import json
    config_file = config_dir / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(AUTOGEN_CONFIG, f, indent=2, ensure_ascii=False)
    
    print(f"AutoGen Studio configuration saved to: {config_file}")
    return config_file

if __name__ == "__main__":
    create_autogen_studio_config()
