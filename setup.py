#!/usr/bin/env python3
"""
Interruptr 配置检查和初始化脚本
"""

import os
import sys
from pathlib import Path
import shutil

def create_env_file():
    """创建环境配置文件"""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if not env_file.exists() and env_example.exists():
        print("🔧 创建环境配置文件...")
        shutil.copy(env_example, env_file)
        print(f"✅ 已创建 {env_file}")
        print("⚠️  请编辑 .env 文件并添加您的API密钥")
        return False
    elif env_file.exists():
        print(f"✅ 环境配置文件已存在: {env_file}")
        return True
    else:
        print("❌ 缺少环境配置模板文件")
        return False

def check_api_keys():
    """检查API密钥配置"""
    from config.env_config import config
    
    print("\n🔑 检查API密钥配置...")
    
    openai_configured = bool(config.openai_api_key and config.openai_api_key != 'your-openai-api-key-here')
    anthropic_configured = bool(config.anthropic_api_key and config.anthropic_api_key != 'your-anthropic-api-key-here')
    
    if openai_configured:
        print("✅ OpenAI API密钥已配置")
    else:
        print("⚠️  OpenAI API密钥未配置")
    
    if anthropic_configured:
        print("✅ Anthropic API密钥已配置")
    else:
        print("⚠️  Anthropic API密钥未配置")
    
    if not openai_configured and not anthropic_configured:
        print("❌ 请至少配置一个LLM API密钥")
        print("   在 .env 文件中设置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY")
        return False
    
    return True

def check_system_tools():
    """检查系统工具"""
    from config.env_config import config
    
    print("\n🛠️  检查系统工具...")
    
    tools = {
        'GCC': config.gcc_path,
        'GDB': config.gdb_path, 
        'Valgrind': config.valgrind_path,
        'Cppcheck': config.cppcheck_path,
        'Clang': config.clang_path
    }
    
    all_available = True
    for tool_name, tool_path in tools.items():
        if Path(tool_path).exists():
            print(f"✅ {tool_name}: {tool_path}")
        else:
            print(f"❌ {tool_name}: {tool_path} (不存在)")
            all_available = False
    
    if not all_available:
        print("\n安装缺失的工具:")
        print("sudo apt install -y gcc gdb valgrind cppcheck clang-tools")
    
    return all_available

def check_python_packages():
    """检查Python包"""
    print("\n📦 检查Python依赖包...")
    
    required_packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('streamlit', 'Streamlit'),
        ('autogen_agentchat', 'AutoGen'),
        ('langgraph', 'LangGraph'),
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('plotly', 'Plotly'),
        ('networkx', 'NetworkX')
    ]
    
    missing_packages = []
    
    for package, display_name in required_packages:
        try:
            __import__(package)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少包: {', '.join(missing_packages)}")
        print("运行: pip install -r requirements.txt")
        return False
    
    return True

def create_directories():
    """创建必要的目录"""
    print("\n📁 创建项目目录...")
    
    directories = [
        'logs',
        'uploads', 
        'temp',
        'data'
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建目录: {directory}")
        else:
            print(f"📁 目录已存在: {directory}")

def validate_configuration():
    """验证完整配置"""
    print("\n🔍 验证配置...")
    
    try:
        from config.env_config import config
        validation = config.validate_config()
        
        if validation['valid']:
            print("✅ 配置验证通过")
            
            # 显示配置摘要
            summary = validation['config_summary']
            print("\n📋 配置摘要:")
            print(f"  默认LLM: {summary['llm_providers']['default']}")
            print(f"  API地址: {summary['api_config']['host']}:{summary['api_config']['port']}")
            print(f"  安全级别: {summary['security_level']}")
            print(f"  最大文件: {summary['max_file_size']}")
            
            return True
        else:
            print("❌ 配置验证失败:")
            for issue in validation['issues']:
                print(f"  - {issue}")
            return False
            
    except Exception as e:
        print(f"❌ 配置验证错误: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Interruptr 配置检查和初始化")
    print("=" * 50)
    
    # 检查当前目录
    if not Path('config').exists():
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 执行检查步骤
    steps = [
        ("创建环境文件", create_env_file),
        ("检查Python包", check_python_packages),
        ("创建目录结构", create_directories),
        ("检查系统工具", check_system_tools),
        ("检查API密钥", check_api_keys),
        ("验证配置", validate_configuration)
    ]
    
    all_passed = True
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        try:
            if not step_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {step_name} 失败: {e}")
            all_passed = False
    
    # 总结
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有检查通过！项目配置完成")
        print("\n下一步:")
        print("1. 编辑 .env 文件添加API密钥")
        print("2. 运行 ./start.sh 启动服务")
    else:
        print("⚠️  部分检查未通过，请根据上述提示解决问题")
        
    print("\n配置帮助:")
    print("- 环境配置: 编辑 .env 文件")
    print("- 启动服务: ./start.sh")
    print("- 查看文档: README.md")

if __name__ == "__main__":
    main()
