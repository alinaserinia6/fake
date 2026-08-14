#!/usr/bin/env python3
"""
Interruptr System Startup Script
Provides complete system startup and management functionality
"""

import asyncio
import subprocess
import sys
import time
import signal
import threading
from pathlib import Path

# Add project root directory to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from config.env_config import config

class InterruptrLauncher:
    """Interruptr system launcher"""
    
    def __init__(self):
        self.processes = {}
        self.running = False
        
    def check_dependencies(self):
        """Check system dependencies"""
        print("🔍 Checking system dependencies...")
        
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
            print("❌ Missing required files:")
            for file_path in missing_files:
                print(f"  - {file_path}")
            return False
        
        print("✅ All required files exist")
        return True
    
    def check_python_packages(self):
        """Check Python packages"""
        print("\n📦 Checking Python packages...")
        
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
                # Special handling for package name mapping
                import_name = package.replace("-", "_")
                if package == "python-dotenv":
                    import_name = "dotenv"
                __import__(import_name)
                print(f"  ✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"  ❌ {package}")
        
        if missing_packages:
            print(f"\n⚠️ Missing packages, recommended installation:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
        
        print("✅ All required packages installed")
        return True
    
    def start_api_server(self):
        """Start the API server"""
        print("\n🚀 Starting API server...")
        
        try:
            # Create log directory
            log_dir = project_root / "logs"
            log_dir.mkdir(exist_ok=True)
            
            # Start uvicorn server
            cmd = [
                sys.executable, "-m", "uvicorn",
                "api.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ]
            
            # Open log files
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
            
            # Wait for service to start
            time.sleep(3)
            
            if process.poll() is None:
                print("✅ API server started successfully (http://localhost:8000)")
                print(f"📝 Log file: {log_dir}/api.log")
                return True
            else:
                print("❌ API server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ API server startup exception: {e}")
            return False
    
    def start_frontend(self):
        """Start the frontend interface"""
        print("\n🖥️ Starting frontend interface...")
        
        try:
            # Create log directory
            log_dir = project_root / "logs"
            log_dir.mkdir(exist_ok=True)
            
            # Start Streamlit application
            cmd = [
                sys.executable, "-m", "streamlit", "run",
                "frontend/app.py",
                "--server.port", "8501",
                "--server.address", "0.0.0.0",
                "--server.headless", "true"
            ]
            
            # Open log files
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
            
            # Wait for service to start
            time.sleep(5)
            
            if process.poll() is None:
                print("✅ Frontend interface started successfully (http://localhost:8501)")
                print(f"📝 Log file: {log_dir}/frontend.log")
                return True
            else:
                print("❌ Frontend interface failed to start")
                print(f"❌ Check error log: {log_dir}/frontend_error.log")
                return False
                
        except Exception as e:
            print(f"❌ Frontend interface startup exception: {e}")
            return False
    
    def monitor_processes(self):
        """Monitor process status"""
        while self.running:
            for name, obj in self.processes.items():
                # Only monitor process objects, skip file objects
                if hasattr(obj, 'poll') and obj.poll() is not None:
                    print(f"⚠️ {name} process has stopped")
            time.sleep(10)
    
    def stop_all(self):
        """Stop all services"""
        print("\n🛑 Stopping all services...")
        self.running = False
        
        # First stop processes
        for name, process in list(self.processes.items()):
            if hasattr(process, 'terminate'):  # This is a process
                try:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ {name} stopped")
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"🔫 Force stopped {name}")
                except Exception as e:
                    print(f"❌ Failed to stop {name}: {e}")
        
        # Close log files
        for name, file_obj in list(self.processes.items()):
            if hasattr(file_obj, 'close'):  # This is a file object
                try:
                    file_obj.close()
                    print(f"📄 Closed log file {name}")
                except Exception as e:
                    print(f"❌ Failed to close log file {name}: {e}")
        
        self.processes.clear()
    
    def signal_handler(self, signum, frame):
        """Signal handler"""
        print(f"\nReceived signal {signum}, stopping...")
        self.stop_all()
        sys.exit(0)
    
    def run(self):
        """Run the full system"""
        print("🎯 Interruptr Multi-Agent System Launcher")
        print("=" * 50)
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed, please verify file integrity")
            return False
        
        if not self.check_python_packages():
            print("❌ Package check failed, please install required dependencies")
            return False
        
        # Display configuration information
        print(f"\n⚙️ Configuration:")
        print(f"  - OpenAI model: {config.openai_model}")
        print(f"  - Claude model: {config.anthropic_model}")
        print(f"  - Gemini model: {config.gemini_model}")
        print(f"  - Ollama model: {config.ollama_model}")
        
        # Start services
        if not self.start_api_server():
            print("❌ API server failed to start")
            return False
        
        if not self.start_frontend():
            print("❌ Frontend interface failed to start")
            self.stop_all()
            return False
        
        # Start monitoring
        self.running = True
        monitor_thread = threading.Thread(target=self.monitor_processes)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        print("\n🎉 System startup complete!")
        print("📍 Access URLs:")
        print("  - Frontend interface: http://localhost:8501")
        print("  - API docs: http://localhost:8000/docs")
        print("\n📝 Log files:")
        print("  - API logs: logs/api.log")
        print("  - Frontend logs: logs/frontend.log")
        print("  - Error logs: logs/*_error.log")
        print("\n🔍 Commands to view logs:")
        print("  - tail -f logs/api.log          # Real-time API logs")
        print("  - tail -f logs/frontend.log     # Real-time frontend logs")
        print("  - tail -f logs/*_error.log      # Real-time error logs")
        print("\n💡 Usage instructions:")
        print("  1. Upload a C/C++ file in the frontend interface")
        print("  2. Select analysis mode and agent configuration")
        print("  3. Start multi-agent analysis")
        print("  4. View visualised results and detailed reports")
        print("\nPress Ctrl+C to stop the system")
        
        try:
            # Keep running
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutdown signal received...")
        finally:
            self.stop_all()
        
        return True

def main():
    """Main function"""
    launcher = InterruptrLauncher()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            # Run tests
            print("🧪 Running system tests...")
            import test_system
            asyncio.run(test_system.main())
        
        elif command == "config":
            # Display configuration
            print("⚙️ Current configuration:")
            print(f"  OpenAI API: {'Configured' if config.openai_api_key else 'Not configured'}")
            print(f"  Claude API: {'Configured' if config.anthropic_api_key else 'Not configured'}")
            print(f"  Gemini API: {'Configured' if config.gemini_api_key else 'Not configured'}")
            print(f"  Ollama: {'Configured' if config.ollama_base_url else 'Not configured'}")
        
        elif command == "demo":
            # Run demo
            print("🎪 Starting demo mode...")
            launcher.run()
        
        elif command == "help":
            print("📖 Interruptr Usage Instructions:")
            print("  python start.py          - Start the full system")
            print("  python start.py test     - Run system tests")
            print("  python start.py config   - Display configuration")
            print("  python start.py demo     - Demo mode")
            print("  python start.py help     - Show this help")
        
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'python start.py help' for assistance")
    
    else:
        # Default: start the full system
        launcher.run()

if __name__ == "__main__":
    main()
