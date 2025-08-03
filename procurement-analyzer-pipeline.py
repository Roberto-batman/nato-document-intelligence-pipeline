# NATO Procurement Document Intelligence Pipeline
# AI-900 Exam Preparation Project

"""
This project demonstrates key AI-900 concepts:
1. Document Intelligence (Form Recognizer)
2. Text Analytics (Cognitive Services)
3. Machine Learning Classification
4. Responsible AI Implementation
"""

# Required libraries for the project
import os
import json
import pandas as pd
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Azure SDK components for AI-900 services
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient

print("📋 NATO Document Intelligence Pipeline - Setup Complete")
print("🎯 AI-900 Learning Focus: Cognitive Services Integration")
print("=" * 60)

class NATODocumentProcessor:
    """
    AI-900 Concept: This class demonstrates how to structure
    an AI solution using Azure Cognitive Services
    """
    
    def __init__(self):
        # Initialize Azure service clients
        self.form_recognizer_client = None
        self.text_analytics_client = None
        self.processed_documents = []
        
        print("✅ Document Processor initialized")
        print("📚 AI-900 Tip: Always initialize clients with proper error handling")
    
    def setup_azure_services(self, form_recognizer_key, form_recognizer_endpoint, 
                           text_analytics_key, text_analytics_endpoint):
        """
        AI-900 Learning Point: Setting up Cognitive Services
        - Form Recognizer: Document Intelligence service
        - Text Analytics: Natural Language Processing service
        """
        try:
            # Set up Form Recognizer (Document Intelligence)
            self.form_recognizer_client = DocumentAnalysisClient(
                endpoint=form_recognizer_endpoint,
                credential=AzureKeyCredential(form_recognizer_key)
            )
            
            # Set up Text Analytics
            self.text_analytics_client = TextAnalyticsClient(
                endpoint=text_analytics_endpoint,
                credential=AzureKeyCredential(text_analytics_key)
            )
            
            print("✅ Azure Cognitive Services connected successfully")
            print("🎯 AI-900 Concept: Multi-service AI solution architecture")
            
        except Exception as e:
            print(f"❌ Error setting up Azure services: {str(e)}")
            print("💡 AI-900 Tip: Always implement proper error handling")
    
    def create_sample_nato_data(self):
        """
        Since we're working in a few hours, let's create realistic
        NATO procurement sample data based on public information
        """
        sample_documents = [
            {
                "doc_id": "NATO-PROC-2024-001",
                "title": "IT Infrastructure Modernization - Allied Command Operations",
                "content": """
                CONTRACT AWARD NOTICE
                Contract Title: IT Infrastructure Modernization for Allied Command Operations
                Contract Value: €2,450,000
                Duration: 24 months
                Contractor: TechSecure Solutions Ltd.
                Classification: NATO UNCLASSIFIED
                Risk Level: Medium
                Project Category: Information Technology
                Key Requirements: Cybersecurity compliance, GDPR adherence, 24/7 support
                Strategic Importance: High - Critical infrastructure upgrade
                """,
                "document_type": "contract_award",
                "classification": "UNCLASSIFIED",
                "value": 2450000
            },
            {
                "doc_id": "NATO-PROC-2024-002", 
                "title": "Training Equipment Procurement - NATO Defense College",
                "content": """
                PROCUREMENT REQUEST
                Project: Advanced Training Simulators for NATO Defense College
                Estimated Value: €890,000
                Timeline: 18 months
                Requirements: VR/AR capabilities, multilingual support, NATO standards compliance
                Risk Assessment: Low-Medium
                Strategic Priority: Medium
                Environmental Considerations: Energy efficient systems required
                """,
                "document_type": "procurement_request",
                "classification": "UNCLASSIFIED", 
                "value": 890000
            },
            {
                "doc_id": "NATO-PROC-2024-003",
                "title": "Cybersecurity Assessment Services - NATO HQ",
                "content": """
                SERVICE CONTRACT
                Service: Comprehensive Cybersecurity Assessment
                Contract Value: €1,200,000
                Scope: Penetration testing, vulnerability assessment, compliance audit
                Security Clearance Required: NATO SECRET
                Risk Level: High - Critical security infrastructure
                Compliance Requirements: ISO 27001, NIST Framework
                Deliverables: Risk assessment report, mitigation strategies, training materials
                """,
                "document_type": "service_contract",
                "classification": "UNCLASSIFIED",
                "value": 1200000
            }
        ]
        
        self.sample_data = sample_documents
        print("✅ Sample NATO procurement data created")
        print(f"📊 Generated {len(sample_documents)} sample documents")
        print("🎯 AI-900 Concept: Working with structured and unstructured data")
        
        return sample_documents

# Initialize the processor
processor = NATODocumentProcessor()
sample_docs = processor.create_sample_nato_data()

print("\n" + "=" * 60)
print("🚀 Ready to proceed to document analysis!")
print("📚 Next: We'll extract key information using Azure Form Recognizer")