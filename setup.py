#!/usr/bin/env python3
"""
Setup script for Discord Bot
Helps users configure their bot for first-time use
"""

import os
import sys
import shutil

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if not os.path.exists('.env.example'):
        print("❌ .env.example not found")
        return False
    
    try:
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file and add your Discord bot token")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, you have {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import discord
        import dotenv
        import aiohttp
        import pytz
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e.name}")
        print("Run: pip install -r requirements.txt")
        return False

def main():
    print("🤖 Discord Bot Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing dependencies...")
        os.system("pip install -r requirements.txt")
        
        # Re-check after installation
        if not check_dependencies():
            print("❌ Failed to install dependencies")
            sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file and add your Discord bot token")
    print("2. Run: python secure_main.py")
    print("\nFor help getting a bot token:")
    print("https://discord.com/developers/applications")

if __name__ == "__main__":
    main()
