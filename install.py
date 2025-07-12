#!/usr/bin/env python3
"""
Installation script for the Email Segregation System
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and return success status"""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with error: {e}")
        return False

def check_python():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not supported. Requires Python 3.7+")
        return False

def check_pip():
    """Check if pip is available"""
    print("🔍 Checking pip availability...")
    try:
        import pip
        print("✅ pip is available")
        return True
    except ImportError:
        print("❌ pip is not available")
        return False

def install_dependencies():
    """Install Python dependencies"""
    if not check_pip():
        print("❌ Cannot install dependencies without pip")
        return False
    
    return run_command("python -m pip install -r requirements.txt", "Installing Python dependencies")

def check_mongodb():
    """Check if MongoDB is available"""
    print("🔍 Checking MongoDB availability...")
    try:
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("✅ MongoDB is available and running")
        return True
    except:
        print("⚠️  MongoDB is not available or not running")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('.env.template'):
        print("📝 Creating .env file from template...")
        shutil.copy('.env.template', '.env')
        print("✅ .env file created")
        print("⚠️  Please update the .env file with your actual credentials")
        return True
    else:
        print("❌ .env.template file not found")
        return False

def test_system():
    """Test the system"""
    print("🧪 Testing the system...")
    try:
        # Test basic imports
        sys.path.append('src')
        sys.path.append('config')
        
        from config.settings import Config
        print("✅ Configuration module loaded")
        
        # Test simple demo
        result = subprocess.run([sys.executable, 'simple_demo.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Simple demo test passed")
            return True
        else:
            print("❌ Simple demo test failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    """Main installation process"""
    print("🚀 Email Segregation System Installation")
    print("=" * 50)
    
    success_count = 0
    total_checks = 0
    
    # Check Python version
    total_checks += 1
    if check_python():
        success_count += 1
    
    # Check pip
    total_checks += 1
    if check_pip():
        success_count += 1
    
    # Install dependencies
    total_checks += 1
    if install_dependencies():
        success_count += 1
    
    # Check MongoDB
    total_checks += 1
    if check_mongodb():
        success_count += 1
    else:
        print("💡 MongoDB is optional for the simple demo")
    
    # Create .env file
    total_checks += 1
    if create_env_file():
        success_count += 1
    
    # Test system
    total_checks += 1
    if test_system():
        success_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Installation Results: {success_count}/{total_checks} checks passed")
    
    if success_count >= total_checks - 1:  # Allow MongoDB to be optional
        print("🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        print("1. Update your .env file with actual credentials")
        print("2. Run the simple demo: python simple_demo.py")
        print("3. Run the full system: python main.py")
        print("4. Set up GitHub deployment (see DEPLOYMENT_GUIDE.md)")
        return True
    else:
        print("❌ Installation failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
