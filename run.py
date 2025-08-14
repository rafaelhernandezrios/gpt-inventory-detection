#!/usr/bin/env python3
"""
Startup script for the GPT Image Recognition application
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import requests
        import dotenv
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has API key"""
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your-api-key-here")
        return False
    
    # Check if API key is set
    with open('.env', 'r') as f:
        content = f.read()
        if 'your-api-key-here' in content or 'OPENAI_API_KEY=' not in content:
            print("⚠️  Warning: Please set your actual OpenAI API key in .env file")
            return False
    
    return True

def main():
    """Main startup function"""
    print("🔍 GPT Image Recognition - Startup Check")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 To install dependencies, run:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Check environment file
    env_ok = check_env_file()
    
    print("\n✅ All checks passed!")
    
    if not env_ok:
        print("\n⚠️  You can still run the app, but it may not work without a valid API key")
    
    print("\n🚀 Starting the application...")
    print("=" * 50)
    
    # Import and run the app
    try:
        from app import app, Config
        print(f"🌐 Server will be available at: http://{Config.HOST}:{Config.PORT}")
        print("📱 Open this URL in your browser to use the application")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
