#!/usr/bin/env python3
"""
Interruptr Configuration Check and Initialization Script
"""

import os
import sys
from pathlib import Path
import shutil

def create_env_file():
    """Create environment configuration file"""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if not env_file.exists() and env_example.exists():
        print("🔧 Creating environment configuration file...")
        shutil.copy(env_example, env_file)
        print(f"✅ Created {env_file}")
        print("⚠️  Please edit the .env file and add your API keys")
        return False
    elif env_file.exists():
        print(f"✅ Environment configuration file already exists: {env_file}")
        return True
    else:
        print("❌ Missing environment configuration template file")
        return False

def check_api_keys():
    """Check API key configuration"""
    from config.env_config import config
    
    print("\n🔑 Checking API key configuration...")
    
    openai_configured = bool(config.openai_api_key and config.openai_api_key != 'your-openai-api-key-here')
    anthropic_configured = bool(config.anthropic_api_key and config.anthropic_api_key != 'your-anthropic-api-key-here')
    
    if openai_configured:
        print("✅ OpenAI API key configured")
    else:
        print("⚠️  OpenAI API key not configured")
    
    if anthropic_configured:
        print("✅ Anthropic API key configured")
    else:
        print("⚠️  Anthropic API key not configured")
    
    if not openai_configured and not anthropic_configured:
        print("❌ Please configure at least one LLM API key")
        print("   Set OPENAI_API_KEY or ANTHROPIC_API_KEY in the .env file")
        return False
    
    return True

def check_system_tools():
    """Check system tools"""
    from config.env_config import config
    
    print("\n🛠️  Checking system tools...")
    
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
            print(f"❌ {tool_name}: {tool_path} (does not exist)")
            all_available = False
    
    if not all_available:
        print("\nInstall missing tools:")
        print("sudo apt install -y gcc gdb valgrind cppcheck clang-tools")
    
    return all_available

def check_python_packages():
    """Check Python packages"""
    print("\n📦 Checking Python dependencies...")
    
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
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating project directories...")
    
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
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def validate_configuration():
    """Validate full configuration"""
    print("\n🔍 Validating configuration...")
    
    try:
        from config.env_config import config
        validation = config.validate_config()
        
        if validation['valid']:
            print("✅ Configuration validation passed")
            
            # Display configuration summary
            summary = validation['config_summary']
            print("\n📋 Configuration summary:")
            print(f"  Default LLM: {summary['llm_providers']['default']}")
            print(f"  API address: {summary['api_config']['host']}:{summary['api_config']['port']}")
            print(f"  Security level: {summary['security_level']}")
            print(f"  Max file size: {summary['max_file_size']}")
            
            return True
        else:
            print("❌ Configuration validation failed:")
            for issue in validation['issues']:
                print(f"  - {issue}")
            return False
            
    except Exception as e:
        print(f"❌ Configuration validation error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Interruptr Configuration Check and Initialization")
    print("=" * 50)
    
    # Check current directory
    if not Path('config').exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Run check steps
    steps = [
        ("Create environment file", create_env_file),
        ("Check Python packages", check_python_packages),
        ("Create directory structure", create_directories),
        ("Check system tools", check_system_tools),
        ("Check API keys", check_api_keys),
        ("Validate configuration", validate_configuration)
    ]
    
    all_passed = True
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        try:
            if not step_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {step_name} failed: {e}")
            all_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Project configuration complete")
        print("\nNext steps:")
        print("1. Edit the .env file to add API keys")
        print("2. Run ./start.sh to start the service")
    else:
        print("⚠️  Some checks failed. Please resolve the issues as indicated above")
        
    print("\nConfiguration help:")
    print("- Environment configuration: edit the .env file")
    print("- Start service: ./start.sh")
    print("- View documentation: README.md")

if __name__ == "__main__":
    main()
