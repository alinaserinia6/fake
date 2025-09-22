#!/usr/bin/env python3
"""
Interruptr 系统启动脚本
提供完整的系统启动和管理功能
"""

import asyncio
import subprocess
import sys
import time
import signal
import threading
from pathlib import Path
import json
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from config.env_config import config

class InterruptrLauncher:
    """Interruptr系统启动器"""
    
    def __init__(self):
        self.processes = {}
        self.running = False
        
    def check_dependencies(self):
        """检查系统依赖"""
        print("🔍 检查系统依赖...")
        
        required_files = [
            "config/env_config.py",
            "api/main.py", 
            "frontend/app.py",
            "agents/enhanced_multi_agent_system.py",
            ".env"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
            else:
                print(f"  ✅ {file_path}")
        
        if missing_files:
            print("❌ 缺少必要文件:")
            for file_path in missing_files:
                print(f"  - {file_path}")
            return False
        
        print("✅ 所有必要文件存在")
        return True
    
    def check_python_packages(self):
        """检查Python包"""
        print("\n📦 检查Python包...")
        
        required_packages = [
            "fastapi",
            "uvicorn", 
            "streamlit",
            "openai",
            "anthropic",
            "python-dotenv"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                # 特殊处理包名映射
                import_name = package.replace("-", "_")
                if package == "python-dotenv":
                    import_name = "dotenv"
                __import__(import_name)
                print(f"  ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"  ❌ {package}")
        
        if missing_packages:
            print(f"\n⚠️ 缺少包，建议安装:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
        
        print("✅ 所有必要包已安装")
        return True
    
    def start_api_server(self):
        """启动API服务器"""
        print("\n🚀 启动API服务器...")
        
        try:
            # 创建日志目录
            log_dir = project_root / "logs"
            log_dir.mkdir(exist_ok=True)
            
            # 启动uvicorn服务器
            cmd = [
                sys.executable, "-m", "uvicorn",
                "api.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ]
            
            # 打开日志文件
            api_log = open(log_dir / "api.log", "w", encoding="utf-8")
            api_error = open(log_dir / "api_error.log", "w", encoding="utf-8")
            
            process = subprocess.Popen(
                cmd,
                cwd=project_root,
                stdout=api_log,
                stderr=api_error,
                text=True
            )
            
            self.processes["api"] = process
            self.processes["api_log"] = api_log
            self.processes["api_error"] = api_error
            
            # 等待服务启动
            time.sleep(3)
            
            if process.poll() is None:
                print("✅ API服务器启动成功 (http://localhost:8000)")
                print(f"📝 日志文件: {log_dir}/api.log")
                return True
            else:
                print("❌ API服务器启动失败")
                return False
                
        except Exception as e:
            print(f"❌ API服务器启动异常: {e}")
            return False
    
    def start_frontend(self):
        """启动前端界面"""
        print("\n🖥️ 启动前端界面...")
        
        try:
            # 创建日志目录
            log_dir = project_root / "logs"
            log_dir.mkdir(exist_ok=True)
            
            # 启动Streamlit应用
            cmd = [
                sys.executable, "-m", "streamlit", "run",
                "frontend/app.py",
                "--server.port", "8501",
                "--server.address", "0.0.0.0",
                "--server.headless", "true"
            ]
            
            # 打开日志文件
            frontend_log = open(log_dir / "frontend.log", "w", encoding="utf-8")
            frontend_error = open(log_dir / "frontend_error.log", "w", encoding="utf-8")
            
            process = subprocess.Popen(
                cmd,
                cwd=project_root,
                stdout=frontend_log,
                stderr=frontend_error,
                text=True
            )
            
            self.processes["frontend"] = process
            self.processes["frontend_log"] = frontend_log
            self.processes["frontend_error"] = frontend_error
            
            # 等待服务启动
            time.sleep(5)
            
            if process.poll() is None:
                print("✅ 前端界面启动成功 (http://localhost:8501)")
                print(f"📝 日志文件: {log_dir}/frontend.log")
                return True
            else:
                print("❌ 前端界面启动失败")
                print(f"❌ 检查错误日志: {log_dir}/frontend_error.log")
                return False
                
        except Exception as e:
            print(f"❌ 前端界面启动异常: {e}")
            return False
    
    def monitor_processes(self):
        """监控进程状态"""
        while self.running:
            for name, obj in self.processes.items():
                # 只监控进程对象，跳过文件对象
                if hasattr(obj, 'poll') and obj.poll() is not None:
                    print(f"⚠️ {name} 进程已停止")
            time.sleep(10)
    
    def stop_all(self):
        """停止所有服务"""
        print("\n🛑 停止所有服务...")
        self.running = False
        
        # 先停止进程
        for name, process in list(self.processes.items()):
            if hasattr(process, 'terminate'):  # 这是一个进程
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ {name} 已停止")
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"🔫 强制停止 {name}")
                except Exception as e:
                    print(f"❌ 停止 {name} 失败: {e}")
        
        # 关闭日志文件
        for name, file_obj in list(self.processes.items()):
            if hasattr(file_obj, 'close'):  # 这是一个文件对象
                try:
                    file_obj.close()
                    print(f"📄 关闭日志文件 {name}")
                except Exception as e:
                    print(f"❌ 关闭日志文件 {name} 失败: {e}")
        
        self.processes.clear()
    
    def signal_handler(self, signum, frame):
        """信号处理器"""
        print(f"\n收到信号 {signum}，正在停止...")
        self.stop_all()
        sys.exit(0)
    
    def run(self):
        """运行完整系统"""
        print("🎯 Interruptr 多智能体系统启动器")
        print("=" * 50)
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # 检查依赖
        if not self.check_dependencies():
            print("❌ 依赖检查失败，请检查文件完整性")
            return False
        
        if not self.check_python_packages():
            print("❌ 包检查失败，请安装必要依赖")
            return False
        
        # 显示配置信息
        print(f"\n⚙️ 配置信息:")
        print(f"  - OpenAI模型: {config.openai_model}")
        print(f"  - Claude模型: {config.anthropic_model}")
        print(f"  - Gemini模型: {config.gemini_model}")
        print(f"  - Ollama模型: {config.ollama_model}")
        
        # 启动服务
        if not self.start_api_server():
            print("❌ API服务器启动失败")
            return False
        
        if not self.start_frontend():
            print("❌ 前端界面启动失败")
            self.stop_all()
            return False
        
        # 开始监控
        self.running = True
        monitor_thread = threading.Thread(target=self.monitor_processes)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        print("\n🎉 系统启动完成！")
        print("📍 访问地址:")
        print("  - 前端界面: http://localhost:8501")
        print("  - API文档: http://localhost:8000/docs")
        print("\n� 日志文件:")
        print("  - API日志: logs/api.log")
        print("  - 前端日志: logs/frontend.log")
        print("  - 错误日志: logs/*_error.log")
        print("\n🔍 查看日志命令:")
        print("  - tail -f logs/api.log          # 实时查看API日志")
        print("  - tail -f logs/frontend.log     # 实时查看前端日志")
        print("  - tail -f logs/*_error.log      # 实时查看错误日志")
        print("\n�💡 使用说明:")
        print("  1. 在前端界面上传C/C++文件")
        print("  2. 选择分析模式和智能体配置")
        print("  3. 开始多智能体分析")
        print("  4. 查看可视化结果和详细报告")
        print("\n按 Ctrl+C 停止系统")
        
        try:
            # 保持运行
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n收到停止信号...")
        finally:
            self.stop_all()
        
        return True

def main():
    """主函数"""
    launcher = InterruptrLauncher()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            # 运行测试
            print("🧪 运行系统测试...")
            import test_system
            asyncio.run(test_system.main())
        
        elif command == "config":
            # 显示配置
            print("⚙️ 当前配置:")
            print(f"  OpenAI API: {'已配置' if config.openai_api_key else '未配置'}")
            print(f"  Claude API: {'已配置' if config.anthropic_api_key else '未配置'}")
            print(f"  Gemini API: {'已配置' if config.gemini_api_key else '未配置'}")
            print(f"  Ollama: {'已配置' if config.ollama_base_url else '未配置'}")
        
        elif command == "demo":
            # 运行演示
            print("🎪 启动演示模式...")
            launcher.run()
        
        elif command == "help":
            print("📖 Interruptr 使用说明:")
            print("  python start.py          - 启动完整系统")
            print("  python start.py test     - 运行系统测试")
            print("  python start.py config   - 显示配置信息")
            print("  python start.py demo     - 演示模式")
            print("  python start.py help     - 显示帮助")
        
        else:
            print(f"❌ 未知命令: {command}")
            print("使用 'python start.py help' 查看帮助")
    
    else:
        # 默认启动完整系统
        launcher.run()

if __name__ == "__main__":
    main()
