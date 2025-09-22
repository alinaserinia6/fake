"""
项目配置文件
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# API配置
API_HOST = "localhost"
API_PORT = 8000
API_DEBUG = True

# 大模型配置
LLM_CONFIGS = {
    "openai": {
        "model": "gpt-4",
        "api_key": os.getenv("OPENAI_API_KEY"),
        "temperature": 0.1
    },
    "anthropic": {
        "model": "claude-3-sonnet-20240229", 
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
        "temperature": 0.1
    }
}

# 数据库配置
DATABASE_URL = "sqlite:///./interruptr.db"
REDIS_URL = "redis://localhost:6379"

# 分析工具路径
ANALYSIS_TOOLS = {
    "gcc": "/usr/bin/gcc",
    "gdb": "/usr/bin/gdb", 
    "valgrind": "/usr/bin/valgrind",
    "cppcheck": "/usr/bin/cppcheck",
    "clang": "/usr/bin/clang"
}

# 智能体配置
AGENT_CONFIGS = {
    "coordinator": {
        "name": "协调者",
        "role": "管理和协调其他智能体的工作流程",
        "max_iterations": 10
    },
    "code_analyst": {
        "name": "代码分析师", 
        "role": "静态代码分析和代码质量评估",
        "max_iterations": 5
    },
    "security_expert": {
        "name": "安全专家",
        "role": "安全漏洞检测和分析", 
        "max_iterations": 5
    },
    "debug_expert": {
        "name": "调试专家",
        "role": "断点设置和动态调试分析",
        "max_iterations": 5
    },
    "architect": {
        "name": "架构师",
        "role": "整体架构和设计模式分析",
        "max_iterations": 3
    }
}

# 安全检测规则
SECURITY_RULES = {
    "buffer_overflow": {
        "patterns": ["strcpy", "strcat", "sprintf", "gets"],
        "severity": "high"
    },
    "memory_leak": {
        "patterns": ["malloc", "calloc", "realloc", "new"],
        "severity": "medium"
    },
    "null_pointer": {
        "patterns": ["->", ".", "*"],
        "severity": "medium"
    },
    "integer_overflow": {
        "patterns": ["int", "unsigned", "long"],
        "severity": "medium"
    }
}

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
