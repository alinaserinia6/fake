"""
AutoGen Studio 配置文件 - 多智能体代码分析系统
"""
import os
from pathlib import Path

# AutoGen Studio 配置
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
            "description": "协调器：负责任务分解和流程管理",
            "system_message": """你是一个多智能体系统的协调器。
你的任务是：
1. 接收代码分析请求
2. 将复杂任务分解为子任务
3. 协调各个专家智能体的工作
4. 整合分析结果
5. 提供最终的修复建议

请始终保持专业、准确和高效。""",
            "model": "gpt-4",
            "max_consecutive_auto_reply": 10
        },
        {
            "name": "code_analyst",
            "description": "代码分析专家：专注于代码结构和逻辑分析",
            "system_message": """你是一个专业的代码分析专家。
你的专长包括：
1. 静态代码分析
2. 代码结构评估
3. 逻辑流程分析
4. 代码质量评估
5. 性能瓶颈识别

分析时请提供详细的技术细节和改进建议。""",
            "model": "claude-3-sonnet",
            "max_consecutive_auto_reply": 5
        },
        {
            "name": "security_expert",
            "description": "安全专家：专注于安全漏洞检测",
            "system_message": """你是一个网络安全专家。
你的专长包括：
1. 安全漏洞检测（缓冲区溢出、注入攻击等）
2. 安全代码审计
3. 威胁建模
4. 安全最佳实践
5. 漏洞修复建议

请提供详细的安全分析和修复方案。""",
            "model": "gpt-4",
            "max_consecutive_auto_reply": 5
        },
        {
            "name": "debug_expert",
            "description": "调试专家：专注于错误定位和修复",
            "system_message": """你是一个调试专家。
你的专长包括：
1. 运行时错误分析
2. 内存泄漏检测
3. 死锁和竞态条件分析
4. 性能问题诊断
5. 错误修复方案

请提供精确的错误定位和可行的修复方案。""",
            "model": "gpt-oss",
            "max_consecutive_auto_reply": 5
        },
        {
            "name": "architect",
            "description": "架构师：专注于系统设计和重构建议",
            "system_message": """你是一个软件架构师。
你的专长包括：
1. 系统架构设计
2. 代码重构建议
3. 设计模式应用
4. 可维护性评估
5. 扩展性分析

请提供系统级的改进建议。""",
            "model": "claude-3-sonnet",
            "max_consecutive_auto_reply": 5
        },
        {
            "name": "critic",
            "description": "评审专家：负责质量控制和最终评审",
            "system_message": """你是一个代码评审专家。
你的职责是：
1. 评审其他专家的分析结果
2. 验证修复方案的可行性
3. 提供质量保证
4. 标识遗漏的问题
5. 确保最终方案的完整性

请提供客观、全面的评审意见。""",
            "model": "gpt-4",
            "max_consecutive_auto_reply": 3
        }
    ],
    
    "workflows": [
        {
            "name": "c_cpp_code_analysis",
            "description": "C/C++代码分析流程",
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
            "description": "C++静态代码分析",
            "content": """
def analyze_cpp_code(code_content, file_path):
    '''分析C++代码的静态问题'''
    import subprocess
    import tempfile
    
    # 保存代码到临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
        f.write(code_content)
        temp_file = f.name
    
    results = []
    
    # 编译检查
    try:
        result = subprocess.run(['g++', '-Wall', '-Wextra', '-fsyntax-only', temp_file],
                              capture_output=True, text=True)
        if result.stderr:
            results.append(f"编译警告/错误:\\n{result.stderr}")
    except Exception as e:
        results.append(f"编译检查失败: {e}")
    
    # cppcheck 静态分析
    try:
        result = subprocess.run(['cppcheck', '--enable=all', '--verbose', temp_file],
                              capture_output=True, text=True)
        if result.stderr:
            results.append(f"cppcheck 分析:\\n{result.stderr}")
    except Exception as e:
        results.append(f"cppcheck 分析失败: {e}")
    
    # 清理临时文件
    import os
    os.unlink(temp_file)
    
    return "\\n\\n".join(results) if results else "未发现明显问题"
"""
        }
    ]
}

def create_autogen_studio_config():
    """创建 AutoGen Studio 配置文件"""
    config_dir = Path.home() / ".autogenstudio" 
    config_dir.mkdir(exist_ok=True)
    
    # 写入配置
    import json
    config_file = config_dir / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(AUTOGEN_CONFIG, f, indent=2, ensure_ascii=False)
    
    print(f"AutoGen Studio 配置已保存到: {config_file}")
    return config_file

if __name__ == "__main__":
    create_autogen_studio_config()
