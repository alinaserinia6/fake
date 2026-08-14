#!/usr/bin/env python3
"""
Real multi-agent code analysis demonstration script
Uses AutoGen for multi-agent collaboration
"""

import os
import asyncio
from pathlib import Path
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Configure model
def get_model_client():
    """Get model client - prefer local Ollama"""
    try:
        # Try to use local Ollama gpt-oss model
        client = OpenAIChatCompletionClient(
            model="gpt-oss:latest",
            api_key="ollama",
            base_url="http://localhost:11434/v1"
        )
        return client
    except Exception as e:
        print(f"Ollama connection failed, trying OpenAI: {e}")
        # Fallback to OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return OpenAIChatCompletionClient(
                model="gpt-4o-mini",
                api_key=api_key
            )
        else:
            raise Exception("No valid model configuration found")

def create_agents():
    """Create multi-agent team"""
    model_client = get_model_client()
    
    # Coordinator
    coordinator = AssistantAgent(
        name="coordinator",
        model_client=model_client,
        system_message="""You are the coordinator of a multi-agent code analysis system.

        Your responsibilities:
        1. Receive and understand code analysis tasks
        2. Decompose tasks into specific analysis dimensions
        3. Coordinate the work of each expert agent
        4. Integrate analysis results and provide comprehensive recommendations
        5. Ensure completeness and accuracy of the analysis

        Always remain professional and well-organised."""
    )
    
    # Code analysis expert
    code_analyst = AssistantAgent(
        name="code_analyst", 
        model_client=model_client,
        system_message="""You are a professional code analysis expert.

        Your expertise:
        1. Static code analysis and structural assessment
        2. Code logic flow analysis
        3. Code quality and maintainability evaluation
        4. Performance issue identification
        5. Programming best practice checking

        In your analysis, provide specific line numbers, issue descriptions, and improvement suggestions."""
    )
    
    # Security expert
    security_expert = AssistantAgent(
        name="security_expert",
        model_client=model_client, 
        system_message="""You are a cybersecurity expert specialising in code security analysis.

        Your expertise:
        1. Buffer overflow detection
        2. Injection attack vulnerability identification
        3. Memory safety issue analysis
        4. Input validation checking
        5. Secure coding practice evaluation

        Provide detailed security risk assessments and remediation recommendations."""
    )
    
    # Debug expert
    debug_expert = AssistantAgent(
        name="debug_expert",
        model_client=model_client,
        system_message="""You are a debugging and error analysis expert.

        Your expertise:
        1. Runtime error analysis
        2. Memory leak detection
        3. Logic error identification
        4. Exception handling analysis
        5. Error remediation plan design

        Provide precise error localisation and actionable remediation steps."""
    )
    
    # Review expert
    critic = AssistantAgent(
        name="critic",
        model_client=model_client,
        system_message="""You are a code review expert responsible for quality control.

        Your responsibilities:
        1. Review the analysis results of other experts
        2. Verify the accuracy and completeness of the analysis
        3. Identify potentially missed issues
        4. Assess the feasibility of remediation plans
        5. Provide final quality assurance

        Give objective and comprehensive review comments."""
    )
    
    # User proxy - simplified version (not needed in newer versions)
    user_proxy = None
    
    return [coordinator, code_analyst, security_expert, debug_expert, critic], user_proxy

async def analyze_code_with_agents(code_content, file_path):
    """Analyse code using multi-agent system"""
    print(f"\n{'='*60}")
    print(f"Starting multi-agent analysis: {file_path}")
    print(f"{'='*60}")
    
    agents, user_proxy = create_agents()
    
    # Create analysis task
    task_message = f"""
    Please analyse the following C++ code file: {file_path}

    Code content:
    ```cpp
    {code_content}
    ```

    Requirements:
    1. Code analysis expert: perform static analysis and structural assessment
    2. Security expert: check for security vulnerabilities
    3. Debug expert: identify potential runtime errors
    4. Review expert: conduct comprehensive review of all analysis results
    5. Coordinator: synthesise all opinions and provide final remediation recommendations

    Each expert should provide detailed analysis and specific remediation plans.
    """
    
    # Create group chat team
    group_chat = RoundRobinGroupChat(
        participants=agents,
        termination_condition=MaxMessageTermination(max_messages=20)
    )
    
    console = Console(stream=True)
    
    # Start multi-agent conversation
    result = await console.a_run(
        task=task_message,
        team=group_chat
    )
    
    return result

async def main():
    """Main function"""
    print("🤖 Starting multi-agent code analysis system...")
    print("📝 Using AutoGen for real agent collaboration\n")
    
    # Get sample code files
    examples_dir = Path("/home/coder-gw/Interruptr/examples")
    cpp_files = list(examples_dir.glob("*.cpp"))
    
    if not cpp_files:
        print("❌ No sample code files found")
        return
    
    # Analyse each code file
    for cpp_file in cpp_files[:2]:  # Analyse first two files as demonstration
        try:
            with open(cpp_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # Start multi-agent analysis
            await analyze_code_with_agents(code_content, cpp_file.name)
            
            print(f"\n✅ Analysis complete: {cpp_file.name}")
            print("-" * 60)
            
        except Exception as e:
            print(f"❌ Analysis failed for {cpp_file.name}: {e}")
    
    print("\n🎉 Multi-agent analysis complete!")
    print("🌐 AutoGen Studio is running at: http://localhost:8081")

if __name__ == "__main__":
    asyncio.run(main())
