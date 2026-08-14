"""
Project Configuration File
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# API Configuration
API_HOST = "localhost"
API_PORT = 8000
API_DEBUG = True

# LLM Configuration
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

# Database Configuration
DATABASE_URL = "sqlite:///./interruptr.db"
REDIS_URL = "redis://localhost:6379"

# Analysis Tool Paths
ANALYSIS_TOOLS = {
    "gcc": "/usr/bin/gcc",
    "gdb": "/usr/bin/gdb", 
    "valgrind": "/usr/bin/valgrind",
    "cppcheck": "/usr/bin/cppcheck",
    "clang": "/usr/bin/clang"
}

# Agent Configuration
AGENT_CONFIGS = {
    "coordinator": {
        "name": "Coordinator",
        "role": "Manages and coordinates the workflow of other agents",
        "max_iterations": 10
    },
    "code_analyst": {
        "name": "Code Analyst", 
        "role": "Static code analysis and code quality assessment",
        "max_iterations": 5
    },
    "security_expert": {
        "name": "Security Expert",
        "role": "Security vulnerability detection and analysis", 
        "max_iterations": 5
    },
    "debug_expert": {
        "name": "Debug Expert",
        "role": "Breakpoint placement and dynamic debugging analysis",
        "max_iterations": 5
    },
    "architect": {
        "name": "Architect",
        "role": "Overall architecture and design pattern analysis",
        "max_iterations": 3
    }
}

# Security Detection Rules
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

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
