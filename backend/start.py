"""
SPEAR AI Backend Startup Script
Creates venv, installs dependencies, and starts the FastAPI server
"""

import subprocess
import sys
import os
import platform
import signal

# Backend directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BACKEND_DIR, "venv")

# Determine OS-specific paths
IS_WINDOWS = platform.system() == "Windows"
if IS_WINDOWS:
    VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
    VENV_PIP = os.path.join(VENV_DIR, "Scripts", "pip.exe")
else:
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")
    VENV_PIP = os.path.join(VENV_DIR, "bin", "pip")

# Required packages to check
REQUIRED_PACKAGES = [
    "fastapi",
    "uvicorn",
    "transformers",
    "torch",
    "pydantic",
    "dotenv",
    "openai",
]


def venv_exists() -> bool:
    """Check if virtual environment exists"""
    return os.path.exists(VENV_PYTHON)


def create_venv() -> bool:
    """Create virtual environment"""
    print("[*] Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print("[OK] Virtual environment created!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to create virtual environment: {e}")
        return False


def upgrade_pip() -> bool:
    """Upgrade pip in the virtual environment"""
    print("[*] Upgrading pip...")
    try:
        subprocess.check_call([VENV_PYTHON, "-m", "pip", "install", "--upgrade", "pip", "-q"])
        return True
    except subprocess.CalledProcessError:
        return False


def check_package_installed(package_name: str) -> bool:
    """Check if a package is installed in venv"""
    try:
        result = subprocess.run(
            [VENV_PYTHON, "-c", f"import {package_name}"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def check_dependencies() -> bool:
    """Check if all required packages are installed"""
    missing = []
    
    for package in REQUIRED_PACKAGES:
        # Handle package name differences (e.g., 'uvicorn[standard]' -> 'uvicorn')
        import_name = package.split("[")[0]
        if not check_package_installed(import_name):
            missing.append(package)
    
    if missing:
        print(f"[!] Missing packages: {', '.join(missing)}")
        return False
    
    return True


def install_requirements() -> bool:
    """Install all requirements from requirements.txt"""
    requirements_path = os.path.join(BACKEND_DIR, "requirements.txt")
    
    print("[*] Installing dependencies from requirements.txt...")
    print("[*] This may take a few minutes on first run...")
    print()
    try:
        subprocess.check_call([VENV_PIP, "install", "-r", requirements_path])
        print()
        print("[OK] Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print()
        print(f"[ERROR] Failed to install dependencies (exit code: {e.returncode})")
        return False


def start_server():
    """Start the FastAPI server using venv Python"""
    print("[*] Starting SPEAR AI Backend Server...")
    print("[*] Press Ctrl+C to stop")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir(BACKEND_DIR)
    
    # Run uvicorn using venv Python with proper signal handling
    process = None
    try:
        # On Windows, use CREATE_NEW_PROCESS_GROUP for proper Ctrl+C handling
        if IS_WINDOWS:
            process = subprocess.Popen(
                [VENV_PYTHON, "-m", "uvicorn", 
                 "main:app", 
                 "--host", "0.0.0.0", 
                 "--port", "8000", 
                 "--reload"],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            process = subprocess.Popen(
                [VENV_PYTHON, "-m", "uvicorn", 
                 "main:app", 
                 "--host", "0.0.0.0", 
                 "--port", "8000", 
                 "--reload"]
            )
        
        process.wait()
    except KeyboardInterrupt:
        print("\n[*] Shutting down server...")
        if process:
            if IS_WINDOWS:
                process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                process.terminate()
            process.wait()
        print("[OK] Server stopped")


def main():
    print("=" * 50)
    print("   SPEAR AI - Backend Startup")
    print("=" * 50)
    print()
    
    # Step 1: Check/create virtual environment
    if not venv_exists():
        print("[!] Virtual environment not found")
        if not create_venv():
            print("[ERROR] Could not create virtual environment")
            sys.exit(1)
        upgrade_pip()
    else:
        print("[OK] Virtual environment found")
    
    print()
    
    # Step 2: Check/install dependencies
    print("[*] Checking dependencies...")
    
    if not check_dependencies():
        if not install_requirements():
            print("[ERROR] Could not install dependencies. Please install manually:")
            print(f"        {VENV_PIP} install -r requirements.txt")
            sys.exit(1)
        
        # Verify installation
        if not check_dependencies():
            print("[ERROR] Dependencies still missing after installation.")
            sys.exit(1)
    else:
        print("[OK] All dependencies are installed!")
    
    print()
    
    # Step 3: Start the server
    start_server()


if __name__ == "__main__":
    main()
