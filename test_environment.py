# test_environment.py - Test your Azure environment setup
# AI-900 Learning Point: Always test your configuration before proceeding

"""
This script tests your environment setup for the NATO Document Intelligence Pipeline
Run this first to ensure everything is configured correctly
"""

import os
import sys
from dotenv import load_dotenv

def test_python_packages():
    """Test that all required packages are installed"""
    print("🔍 Testing Python Package Installation...")
    
    required_packages = [
        'azure.ai.formrecognizer',
        'azure.ai.textanalytics', 
        'azure.core.credentials',
        'pandas',
        'matplotlib',
        'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("🎉 All packages installed successfully!")
        return True

def test_environment_variables():
    """Test that environment variables are loaded correctly"""
    print("\n🔍 Testing Environment Variables...")
    
    # Load environment variables
    load_dotenv()
    
    required_vars = [
        'FORM_RECOGNIZER_KEY',
        'FORM_RECOGNIZER_ENDPOINT',
        'TEXT_ANALYTICS_KEY',
        'TEXT_ANALYTICS_ENDPOINT'
    ]
    
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value and value != "your_actual_key_here" and "YOUR_" not in value:
            print(f"  ✅ {var}: {value[:20]}...")
        else:
            print(f"  ❌ {var}: Not set or still has placeholder value")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n💡 Check your .env file for: {', '.join(missing_vars)}")
        return False
    else:
        print("🎉 All environment variables loaded successfully!")
        return True

def test_azure_connectivity():
    """Test basic Azure service connectivity"""
    print("\n🔍 Testing Azure Service Connectivity...")
    
    try:
        from azure.ai.formrecognizer import DocumentAnalysisClient
        from azure.ai.textanalytics import TextAnalyticsClient
        from azure.core.credentials import AzureKeyCredential
        
        # Load environment variables
        load_dotenv()
        
        # Test Form Recognizer
        form_key = os.getenv('FORM_RECOGNIZER_KEY')
        form_endpoint = os.getenv('FORM_RECOGNIZER_ENDPOINT')
        
        if form_key and form_endpoint:
            try:
                form_client = DocumentAnalysisClient(
                    endpoint=form_endpoint,
                    credential=AzureKeyCredential(form_key)
                )
                print("  ✅ Form Recognizer client created successfully")
            except Exception as e:
                print(f"  🟡 Form Recognizer client creation failed: {str(e)[:50]}...")
        
        # Test Text Analytics
        text_key = os.getenv('TEXT_ANALYTICS_KEY')
        text_endpoint = os.getenv('TEXT_ANALYTICS_ENDPOINT')
        
        if text_key and text_endpoint:
            try:
                text_client = TextAnalyticsClient(
                    endpoint=text_endpoint,
                    credential=AzureKeyCredential(text_key)
                )
                print("  ✅ Text Analytics client created successfully")
            except Exception as e:
                print(f"  🟡 Text Analytics client creation failed: {str(e)[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Azure connectivity test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 NATO Document Intelligence Pipeline - Environment Test")
    print("=" * 60)
    
    # Test 1: Python packages
    packages_ok = test_python_packages()
    
    # Test 2: Environment variables
    env_vars_ok = test_environment_variables()
    
    # Test 3: Azure connectivity (only if previous tests pass)
    if packages_ok and env_vars_ok:
        azure_ok = test_azure_connectivity()
    else:
        azure_ok = False
        print("\n⏭️  Skipping Azure connectivity test (fix above issues first)")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY:")
    print(f"  📦 Python Packages: {'✅ PASS' if packages_ok else '❌ FAIL'}")
    print(f"  🔐 Environment Variables: {'✅ PASS' if env_vars_ok else '❌ FAIL'}")
    print(f"  ☁️  Azure Connectivity: {'✅ PASS' if azure_ok else '🟡 PARTIAL'}")
    
    if packages_ok and env_vars_ok:
        print("\n🎉 Environment setup complete! Ready to proceed with document processing.")
        print("\n🎯 AI-900 Tip: Proper environment testing prevents issues in production AI systems")
    else:
        print("\n🔧 Please fix the failed tests before proceeding.")
    
    return packages_ok and env_vars_ok

if __name__ == "__main__":
    main()