# nato-document-intelligence-pipeline
a demo using Azure document intelligence and language services

# NATO Document Intelligence Pipeline

An AI-powered document processing pipeline designed for NATO procurement analysis, demonstrating Azure Cognitive Services integration and AI-900 fundamentals.

## 🎯 Project Overview

This project showcases the implementation of an intelligent document processing system using Azure Cognitive Services, specifically designed for analyzing NATO procurement documents. It demonstrates key AI/ML concepts covered in the Azure AI-900 Fundamentals exam.

## 🚀 Key Features

- **Document Intelligence**: Automated extraction of structured data from procurement documents
- **Text Analytics**: Natural language processing for sentiment analysis and key phrase extraction
- **Classification**: Machine learning-based document categorization
- **Data Visualization**: Interactive dashboards for procurement insights
- **Security-First**: Implements responsible AI practices with secure credential management

## 🛠️ Technologies Used

- **Azure Cognitive Services**
  - Form Recognizer (Document Intelligence)
  - Text Analytics (Language Services)
- **Python** with Azure SDK
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Security**: Environment-based configuration management

## 📋 Prerequisites

- Python 3.8+
- Azure subscription (free tier available)
- Azure Form Recognizer resource
- Azure Text Analytics resource

## ⚡ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Roberto-batman/nato-document-intelligence-pipeline.git
   cd nato-document-intelligence-pipeline
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Azure services**
   - Create a `.env` file with your Azure credentials:
   ```
   FORM_RECOGNIZER_KEY=your_key_here
   FORM_RECOGNIZER_ENDPOINT=your_endpoint_here
   TEXT_ANALYTICS_KEY=your_key_here
   TEXT_ANALYTICS_ENDPOINT=your_endpoint_here
   ```

5. **Run the pipeline**
   ```bash
   python document-analyzer-pipeline.py
   ```

## 🎓 AI-900 Learning Objectives Demonstrated

This project covers key Azure AI-900 exam topics:

- **Cognitive Services Integration**: Multi-service AI solution architecture
- **Document Intelligence**: Automated form and document processing
- **Natural Language Processing**: Text analysis and entity extraction
- **Responsible AI**: Secure credential management and data governance
- **MLOps Practices**: Version control and project organization

## 📊 Sample Results

The pipeline processes NATO procurement documents and extracts:
- Contract values and timelines
- Risk assessments
- Key stakeholders
- Compliance requirements
- Strategic importance ratings

## 🔐 Security & Compliance

- Environment-based credential management
- GDPR-compliant data processing
- NATO security classification handling
- Responsible AI implementation

## 👨‍💼 Professional Context

Developed as part of preparation for:
- Azure AI-900 Fundamentals certification
- NATO cybersecurity and project management roles
- Demonstration of AI engineering capabilities

## 🤝 Contributing

This is a demonstration project for professional portfolio purposes. For suggestions or collaboration opportunities, please reach out via LinkedIn or GitHub.

## 📄 License

MIT License - see LICENSE file for details.

## 📧 Contact

**Roberto** - Management Consultant & Cybersecurity PM  
- GitHub: [@Roberto-batman](https://github.com/Roberto-batman)
- Certifications: PMP, ACP, CISSP, Lean Six Sigma Black Belt

---
*This project demonstrates practical AI implementation skills for enterprise and government applications.*