"""
环境变量配置管理器
"""

import os
from pathlib import Path
from typing import Optional
import logging

class EnvConfig:
    """环境变量配置管理"""
    
    def __init__(self, env_file: Optional[str] = None):
        self.env_file = env_file or '.env'
        self.load_env()
        
    def load_env(self):
        """加载环境变量文件"""
        env_path = Path(self.env_file)
        
        if env_path.exists():
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
                logging.info(f"已加载环境配置文件: {env_path}")
            except Exception as e:
                logging.warning(f"加载环境配置文件失败: {e}")
        else:
            logging.warning(f"环境配置文件不存在: {env_path}")
    
    # ================================
    # LLM API 配置
    # ================================
    
    @property
    def openai_api_key(self) -> Optional[str]:
        return os.getenv('OPENAI_API_KEY')
    
    @property
    def openai_model(self) -> str:
        return os.getenv('OPENAI_MODEL', 'gpt-4')
    
    @property
    def openai_base_url(self) -> str:
        return os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
    
    @property
    def openai_temperature(self) -> float:
        return float(os.getenv('OPENAI_TEMPERATURE', '0.1'))
    
    @property
    def openai_max_tokens(self) -> int:
        return int(os.getenv('OPENAI_MAX_TOKENS', '4000'))
    
    @property
    def anthropic_api_key(self) -> Optional[str]:
        return os.getenv('ANTHROPIC_API_KEY')
    
    @property
    def anthropic_model(self) -> str:
        return os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229')
    
    @property
    def anthropic_base_url(self) -> str:
        return os.getenv('ANTHROPIC_BASE_URL', 'https://api.anthropic.com')
    
    @property
    def anthropic_temperature(self) -> float:
        return float(os.getenv('ANTHROPIC_TEMPERATURE', '0.1'))
    
    @property
    def anthropic_max_tokens(self) -> int:
        return int(os.getenv('ANTHROPIC_MAX_TOKENS', '4000'))
    
    @property
    def gemini_api_key(self) -> Optional[str]:
        return os.getenv('GEMINI_API_KEY')
    
    @property
    def gemini_model(self) -> str:
        return os.getenv('GEMINI_MODEL', 'gemini-pro')
    
    @property
    def gemini_base_url(self) -> str:
        return os.getenv('GEMINI_BASE_URL', 'https://generativelanguage.googleapis.com/v1')
    
    @property
    def gemini_temperature(self) -> float:
        return float(os.getenv('GEMINI_TEMPERATURE', '0.2'))
    
    @property
    def gemini_max_tokens(self) -> int:
        return int(os.getenv('GEMINI_MAX_TOKENS', '4000'))
    
    @property
    def ollama_base_url(self) -> str:
        return os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    
    @property
    def ollama_model(self) -> str:
        return os.getenv('OLLAMA_MODEL', 'gpt-oss:latest')
    
    @property
    def ollama_temperature(self) -> float:
        return float(os.getenv('OLLAMA_TEMPERATURE', '0.3'))
    
    @property
    def ollama_max_tokens(self) -> int:
        return int(os.getenv('OLLAMA_MAX_TOKENS', '4000'))
    
    @property
    def default_llm_provider(self) -> str:
        return os.getenv('DEFAULT_LLM_PROVIDER', 'openai')
    
    # ================================
    # 数据库配置
    # ================================
    
    @property
    def database_url(self) -> str:
        return os.getenv('DATABASE_URL', 'sqlite:///./interruptr.db')
    
    @property
    def redis_url(self) -> str:
        return os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    @property
    def redis_password(self) -> Optional[str]:
        return os.getenv('REDIS_PASSWORD')
    
    @property
    def redis_db(self) -> int:
        return int(os.getenv('REDIS_DB', '0'))
    
    # ================================
    # API 服务配置
    # ================================
    
    @property
    def api_host(self) -> str:
        return os.getenv('API_HOST', 'localhost')
    
    @property
    def api_port(self) -> int:
        return int(os.getenv('API_PORT', '8000'))
    
    @property
    def api_debug(self) -> bool:
        return os.getenv('API_DEBUG', 'true').lower() == 'true'
    
    @property
    def api_reload(self) -> bool:
        return os.getenv('API_RELOAD', 'true').lower() == 'true'
    
    @property
    def cors_origins(self) -> list:
        origins = os.getenv('CORS_ORIGINS', '["http://localhost:8501"]')
        import json
        try:
            return json.loads(origins)
        except:
            return ["http://localhost:8501"]
    
    # ================================
    # Streamlit 配置
    # ================================
    
    @property
    def streamlit_host(self) -> str:
        return os.getenv('STREAMLIT_HOST', 'localhost')
    
    @property
    def streamlit_port(self) -> int:
        return int(os.getenv('STREAMLIT_PORT', '8501'))
    
    @property
    def streamlit_debug(self) -> bool:
        return os.getenv('STREAMLIT_DEBUG', 'true').lower() == 'true'
    
    # ================================
    # 智能体配置
    # ================================
    
    @property
    def max_agent_iterations(self) -> int:
        return int(os.getenv('MAX_AGENT_ITERATIONS', '10'))
    
    @property
    def conversation_history_limit(self) -> int:
        return int(os.getenv('CONVERSATION_HISTORY_LIMIT', '100'))
    
    # ================================
    # 智能体角色LLM分配
    # ================================
    
    @property
    def coordinator_llm(self) -> str:
        return os.getenv('COORDINATOR_LLM', 'openai')
    
    @property
    def code_analyst_llm(self) -> str:
        return os.getenv('CODE_ANALYST_LLM', 'claude')
    
    @property
    def security_expert_llm(self) -> str:
        return os.getenv('SECURITY_EXPERT_LLM', 'claude')
    
    @property
    def debug_expert_llm(self) -> str:
        return os.getenv('DEBUG_EXPERT_LLM', 'openai')
    
    @property
    def architect_llm(self) -> str:
        return os.getenv('ARCHITECT_LLM', 'claude')
    
    @property
    def critic_llm(self) -> str:
        return os.getenv('CRITIC_LLM', 'gemini')
    
    @property
    def reviewer_llm(self) -> str:
        return os.getenv('REVIEWER_LLM', 'ollama')
    
    # ================================
    # 分析工具路径
    # ================================
    
    @property
    def gcc_path(self) -> str:
        return os.getenv('GCC_PATH', '/usr/bin/gcc')
    
    @property
    def gdb_path(self) -> str:
        return os.getenv('GDB_PATH', '/usr/bin/gdb')
    
    @property
    def clang_path(self) -> str:
        return os.getenv('CLANG_PATH', '/usr/bin/clang')
    
    @property
    def valgrind_path(self) -> str:
        return os.getenv('VALGRIND_PATH', '/usr/bin/valgrind')
    
    @property
    def cppcheck_path(self) -> str:
        return os.getenv('CPPCHECK_PATH', '/usr/bin/cppcheck')
    
    # ================================
    # 安全检测配置
    # ================================
    
    @property
    def security_level(self) -> str:
        return os.getenv('SECURITY_LEVEL', 'high')
    
    @property
    def max_file_size(self) -> int:
        return int(os.getenv('MAX_FILE_SIZE', '10'))
    
    @property
    def supported_extensions(self) -> list:
        extensions = os.getenv('SUPPORTED_EXTENSIONS', '.c,.cpp,.cc,.cxx,.h,.hpp')
        return [ext.strip() for ext in extensions.split(',')]
    
    # ================================
    # 日志配置
    # ================================
    
    @property
    def log_level(self) -> str:
        return os.getenv('LOG_LEVEL', 'INFO')
    
    @property
    def log_file(self) -> str:
        return os.getenv('LOG_FILE', './logs/interruptr.log')
    
    @property
    def log_format(self) -> str:
        return os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # ================================
    # 可视化配置
    # ================================
    
    @property
    def auto_refresh_interval(self) -> int:
        return int(os.getenv('AUTO_REFRESH_INTERVAL', '5'))
    
    @property
    def chart_theme(self) -> str:
        return os.getenv('CHART_THEME', 'plotly')
    
    @property
    def max_display_messages(self) -> int:
        return int(os.getenv('MAX_DISPLAY_MESSAGES', '50'))
    
    # ================================
    # 验证方法
    # ================================
    
    def validate_config(self) -> dict:
        """验证配置完整性"""
        issues = []
        
        # 检查必需的API密钥
        if not self.openai_api_key and not self.anthropic_api_key and not self.gemini_api_key:
            issues.append("缺少LLM API密钥 (需要OpenAI、Anthropic或Gemini中至少一个)")
        
        # 检查Ollama连接
        try:
            import requests
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            ollama_available = response.status_code == 200
        except:
            ollama_available = False
        
        # 检查工具路径
        tools = {
            'GCC': self.gcc_path,
            'GDB': self.gdb_path,
            'Valgrind': self.valgrind_path,
            'Cppcheck': self.cppcheck_path
        }
        
        for tool_name, tool_path in tools.items():
            if not Path(tool_path).exists():
                issues.append(f"{tool_name} 工具不存在: {tool_path}")
        
        # 检查日志目录
        log_dir = Path(self.log_file).parent
        if not log_dir.exists():
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                issues.append(f"无法创建日志目录: {log_dir}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "config_summary": self.get_config_summary()
        }
    
    def get_config_summary(self) -> dict:
        """获取配置摘要"""
        
        # 检查Ollama可用性
        try:
            import requests
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            ollama_available = response.status_code == 200
        except:
            ollama_available = False
        
        return {
            "llm_providers": {
                "openai": bool(self.openai_api_key),
                "anthropic": bool(self.anthropic_api_key),
                "gemini": bool(self.gemini_api_key), 
                "ollama": ollama_available,
                "default": self.default_llm_provider
            },
            "api_config": {
                "host": self.api_host,
                "port": self.api_port,
                "debug": self.api_debug
            },
            "tools_available": {
                "gcc": Path(self.gcc_path).exists(),
                "gdb": Path(self.gdb_path).exists(),
                "valgrind": Path(self.valgrind_path).exists(),
                "cppcheck": Path(self.cppcheck_path).exists()
            },
            "security_level": self.security_level,
            "max_file_size": f"{self.max_file_size}MB"
        }

# 全局配置实例
config = EnvConfig()

# 导出常用配置
__all__ = ['config', 'EnvConfig']
