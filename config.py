# config.py - Azure Service Configuration
# AI-900 Security Best Practice: Never hardcode keys in your main code!

"""
AI-900 Learning Point: Responsible AI includes secure credential management.
This demonstrates proper secret management practices.
"""

# Create this file as 'config.py' in your project folder
# Replace the placeholder values with your actual Azure keys and endpoints

class AzureConfig:
    """
    Configuration class for Azure Cognitive Services
    
    AI-900 Concept: This demonstrates secure configuration management,
    which is part of Responsible AI practices
    """
    
    # Form Recognizer (Document Intelligence) Configuration
    FORM_RECOGNIZER_KEY = "YOUR_FORM_RECOGNIZER_KEY_HERE"
    FORM_RECOGNIZER_ENDPOINT = "YOUR_FORM_RECOGNIZER_ENDPOINT_HERE"
    
    # Text Analytics (Language Service) Configuration  
    TEXT_ANALYTICS_KEY = "YOUR_TEXT_ANALYTICS_KEY_HERE"
    TEXT_ANALYTICS_ENDPOINT = "YOUR_TEXT_ANALYTICS_ENDPOINT_HERE"
    
    @classmethod
    def validate_config(cls):
        """
        AI-900 Best Practice: Always validate your configuration
        before attempting to connect to Azure services
        """
        missing_configs = []
        
        if "YOUR_" in cls.FORM_RECOGNIZER_KEY:
            missing_configs.append("Form Recognizer Key")
        if "YOUR_" in cls.FORM_RECOGNIZER_ENDPOINT:
            missing_configs.append("Form Recognizer Endpoint")
        if "YOUR_" in cls.TEXT_ANALYTICS_KEY:
            missing_configs.append("Text Analytics Key")
        if "YOUR_" in cls.TEXT_ANALYTICS_ENDPOINT:
            missing_configs.append("Text Analytics Endpoint")
            
        if missing_configs:
            print("❌ Missing Azure Configuration:")
            for config in missing_configs:
                print(f"   - {config}")
            print("\n💡 Update config.py with your Azure service credentials")
            return False
        else:
            print("✅ Azure configuration validated successfully")
            return True

# Environment Variables Approach (More Secure)
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AzureConfig:
    """
    AI-900 Security Best Practice: Using environment variables
    This is the recommended approach for production applications
    """
    FORM_RECOGNIZER_KEY = os.getenv('FORM_RECOGNIZER_KEY')
    FORM_RECOGNIZER_ENDPOINT = os.getenv('FORM_RECOGNIZER_ENDPOINT')
    TEXT_ANALYTICS_KEY = os.getenv('TEXT_ANALYTICS_KEY') 
    TEXT_ANALYTICS_ENDPOINT = os.getenv('TEXT_ANALYTICS_ENDPOINT')

print("📋 Azure Configuration Template Created")
print("🔑 Remember: Keep your API keys secure and never commit them to version control!")
print("🎯 AI-900 Tip: Understanding secure credential management is important for the exam")