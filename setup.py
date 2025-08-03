"""
Setup Script untuk PMO Recovery Bot

Untuk setup awal project, jalankan script ini.
"""

import os
import subprocess
import sys

def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'logs',
        'tests',
        'tests/unit',
        'tests/integration'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    
    return True

def setup_environment():
    """Setup environment file"""
    env_example = ".env.example"
    env_file = ".env"
    
    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print(f"✓ Created {env_file} from {env_example}")
            print("⚠️  Please edit .env file and add your BOT_TOKEN")
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("✓ .env file already exists")
    
    return True

def main():
    """Main setup function"""
    print("🤖 PMO Recovery Bot - Setup Script")
    print("=" * 40)
    
    # Create directories
    create_directories()
    
    # Install dependencies  
    if not install_dependencies():
        return
    
    # Setup environment
    if not setup_environment():
        return
    
    print("\n" + "=" * 40)
    print("✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your BOT_TOKEN from @BotFather")
    print("2. Run: python main.py")
    print("\nFor help, check README.md")

if __name__ == "__main__":
    main()
