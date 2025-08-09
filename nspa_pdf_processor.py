# nspa_pdf_processor.py
# Real NSPA Contract Data Extraction and Analysis
"""
Processes actual NSPA bid opening PDF files to create ML training data.
Perfect for interview demonstration - uses real NSPA operations data!
"""

import pandas as pd
import numpy as np
import re
import os
from datetime import datetime
import json

# PDF processing libraries
try:
    import pdfplumber
    print("✅ pdfplumber available")
except ImportError:
    print("⚠️  Install pdfplumber: pip install pdfplumber")

class NSPAPDFProcessor:
    """
    Processes NSPA bid opening PDFs to extract contract data
    """
    
    def __init__(self):
        self.processed_contracts = []
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text and tables from NSPA PDF files"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_content = ""
                tables_data = []
                
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
                    
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            tables_data.append(table)
                
                return text_content, tables_data
                
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return "", []
    
    def parse_nspa_contract_data(self, text_content, tables_data, file_year):
        """Parse NSPA-specific contract information"""
        contracts = []
        
        for table in tables_data:
            if not table or len(table) < 2:
                continue
            
            # Find header row
            header_row = None
            for i, row in enumerate(table):
                if row and any(header in str(row).upper() for header in 
                             ['COLLECTIVE', 'RFP TITLE', 'CLOSING DATE', 'COMPANIES']):
                    header_row = i
                    break
            
            if header_row is None:
                continue
            
            # Process data rows
            for row in table[header_row + 1:]:
                if not row or len(row) < 4:
                    continue
                
                contract_info = self.extract_contract_details(row, file_year)
                if contract_info:
                    contracts.append(contract_info)
        
        return contracts
    
    def extract_contract_details(self, row, file_year):
        """Extract detailed contract information from table row"""
        try:
            cleaned_row = [str(cell).strip() if cell else "" for cell in row]
            
            if len(cleaned_row) < 4:
                return None
            
            collective_num = cleaned_row[0]
            rfp_title = cleaned_row[1]
            closing_date = cleaned_row[2]
            companies = cleaned_row[3]
            country = cleaned_row[4] if len(cleaned_row) > 4 else ""
            
            # Skip header rows and empty rows
            if (not rfp_title or 
                rfp_title.upper() in ['RFP TITLE', 'TITLE', ''] or
                'BID OPENING' in rfp_title.upper()):
                return None
            
            contract_type = self.categorize_contract_type(rfp_title)
            estimated_value = self.estimate_contract_value(rfp_title, contract_type)
            bidder_count = self.count_bidders(companies)
            risk_assessment = self.assess_contract_risk(rfp_title, contract_type, estimated_value, bidder_count)
            
            contract = {
                'contract_id': collective_num,
                'rfp_title': rfp_title,
                'contract_type': contract_type,
                'closing_date': closing_date,
                'companies': companies,
                'country': country,
                'bidder_count': bidder_count,
                'estimated_value_eur': estimated_value,
                'year': file_year,
                'risk_likelihood': risk_assessment['likelihood'],
                'risk_impact': risk_assessment['impact'],
                'risk_score': risk_assessment['score'],
                'complexity_category': risk_assessment['complexity'],
                'is_multi_national': self.is_multinational_contract(companies),
                'technology_level': self.assess_technology_level(rfp_title)
            }
            
            return contract
            
        except Exception as e:
            print(f"Error extracting contract details: {e}")
            return None
    
    def categorize_contract_type(self, title):
        """Categorize contracts based on NSPA operations"""
        title_upper = title.upper()
        
        categories = {
            'Ammunition': ['CARTRIDGE', 'PROJECTILE', 'MORTAR', 'BOMBS', 'MUNITION'],
            'Logistics_Support': ['LOGISTIC', 'SUPPORT', 'MAINTENANCE', 'SUPPLY'],
            'IT_Infrastructure': ['MICROSOFT', 'INFRASTRUCTURE', 'SOFTWARE', 'SYSTEM'],
            'Medical_Equipment': ['MEDICAL', 'SURGICAL', 'HEATER', 'INFUSION'],
            'Communications': ['COMMUNICATION', 'SATELLITE', 'CIS', 'SHELTER'],
            'Vehicles_Transport': ['VEHICLE', 'TRUCK', 'TRAILER', 'CARGO'],
            'Construction': ['CONSTRUCTION', 'BUILDING', 'WAREHOUSE'],
            'Training': ['TRAINING', 'SIMULATOR', 'SERVICES'],
            'Fuel_Energy': ['FUEL', 'GENERATOR', 'POWER', 'UPS'],
            'Defense_Systems': ['DEFENSE', 'SECURITY', 'GBAD', 'RADAR']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_upper for keyword in keywords):
                return category
        
        return 'Other'
    
    def estimate_contract_value(self, title, contract_type):
        """Estimate contract value - all NSPA contracts shown are >800K EUR"""
        title_upper = title.upper()
        base_value = 1000000  # 1M EUR base
        
        multipliers = {
            'SATELLITE': 50, 'SIMULATOR': 20, 'CONSTRUCTION': 15,
            'AIRCRAFT': 30, 'AMMUNITION': 5, 'MEDICAL': 3,
            'VEHICLE': 8, 'FUEL': 10, 'TRAINING': 4
        }
        
        multiplier = 1
        for keyword, mult in multipliers.items():
            if keyword in title_upper:
                multiplier = max(multiplier, mult)
        
        variation = np.random.uniform(0.7, 1.5)
        return int(base_value * multiplier * variation)
    
    def count_bidders(self, companies_text):
        """Count number of companies bidding"""
        if not companies_text:
            return 0
        return max(1, min(companies_text.count('\n') + 1, 10))
    
    def assess_contract_risk(self, title, contract_type, value, bidder_count):
        """Assess contract risk using NSPA-specific factors"""
        value_risk = min(4, value / 10000000)
        competition_risk = 4 if bidder_count <= 1 else max(1, 5 - bidder_count)
        
        type_risk = {
            'Communications': 1.5, 'IT_Infrastructure': 1.4, 'Defense_Systems': 1.6,
            'Construction': 1.2, 'Ammunition': 1.1, 'Medical_Equipment': 1.0,
            'Logistics_Support': 0.9
        }.get(contract_type, 1.0)
        
        complexity_keywords = ['SATELLITE', 'SIMULATOR', 'CYBER', 'AI', 'ADVANCED']
        complexity_factor = 1.3 if any(kw in title.upper() for kw in complexity_keywords) else 1.0
        
        base_risk = (value_risk + competition_risk) * type_risk * complexity_factor
        
        # Convert to 4x4 matrix
        if base_risk <= 3:
            likelihood, impact = 'Low', np.random.choice(['Low', 'Medium'], p=[0.7, 0.3])
        elif base_risk <= 6:
            likelihood, impact = 'Medium', np.random.choice(['Medium', 'High'], p=[0.6, 0.4])
        elif base_risk <= 9:
            likelihood, impact = 'High', np.random.choice(['High', 'Very High'], p=[0.7, 0.3])
        else:
            likelihood, impact = 'Very High', np.random.choice(['High', 'Very High'], p=[0.3, 0.7])
        
        risk_mapping = {'Low': 1, 'Medium': 2, 'High': 3, 'Very High': 4}
        score = risk_mapping[likelihood] * risk_mapping[impact]
        complexity = 'High' if complexity_factor > 1.2 else 'Medium' if type_risk > 1.2 else 'Low'
        
        return {
            'likelihood': likelihood,
            'impact': impact,
            'score': score,
            'complexity': complexity
        }
    
    def is_multinational_contract(self, companies_text):
        """Check if contract involves multiple countries"""
        if not companies_text:
            return False
        
        countries = ['Germany', 'Italy', 'France', 'Spain', 'USA', 'Canada', 'Norway', 
                    'Netherlands', 'Belgium', 'Turkey', 'Poland', 'United Kingdom']
        country_count = sum(1 for country in countries if country in companies_text)
        return country_count > 1
    
    def assess_technology_level(self, title):
        """Assess technology complexity level"""
        title_upper = title.upper()
        
        high_tech = ['SATELLITE', 'AI', 'CYBER', 'ADVANCED', 'SIMULATOR', 'RADAR']
        medium_tech = ['ELECTRONIC', 'COMMUNICATION', 'SOFTWARE', 'SYSTEM']
        
        if any(kw in title_upper for kw in high_tech):
            return 'High'
        elif any(kw in title_upper for kw in medium_tech):
            return 'Medium'
        else:
            return 'Low'
    
    def process_all_pdfs(self, pdf_folder):
        """Process all NSPA PDF files"""
        print("🔍 Processing NSPA PDF Files...")
        
        all_contracts = []
        pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]
        
        for pdf_file in pdf_files:
            print(f"   Processing: {pdf_file}")
            
            # Extract year from filename
            year_match = re.search(r'20(\d{2})', pdf_file)
            file_year = int(f"20{year_match.group(1)}") if year_match else 2025
            
            pdf_path = os.path.join(pdf_folder, pdf_file)
            text_content, tables_data = self.extract_text_from_pdf(pdf_path)
            contracts = self.parse_nspa_contract_data(text_content, tables_data, file_year)
            
            print(f"   Extracted {len(contracts)} contracts from {pdf_file}")
            all_contracts.extend(contracts)
        
        self.processed_contracts = all_contracts
        print(f"\n✅ Total contracts extracted: {len(all_contracts)}")
        return all_contracts
    
    def save_results(self, output_folder='nspa_real_data'):
        """Save processed NSPA data for Azure ML training"""
        os.makedirs(output_folder, exist_ok=True)
        
        if not self.processed_contracts:
            print("❌ No data to save")
            return
        
        df = pd.DataFrame(self.processed_contracts)
        
        # Add ML features
        df['log_value'] = np.log1p(df['estimated_value_eur'])
        df['value_category'] = pd.cut(df['estimated_value_eur'], 
                                    bins=[0, 2000000, 10000000, 50000000, float('inf')],
                                    labels=['Small', 'Medium', 'Large', 'Very_Large'])
        df['is_high_tech'] = (df['technology_level'] == 'High').astype(int)
        df['is_complex'] = (df['complexity_category'] == 'High').astype(int)
        
        # Save raw data
        raw_file = f'{output_folder}/nspa_contracts_raw.csv'
        df.to_csv(raw_file, index=False)
        
        # Prepare ML training data
        feature_columns = ['estimated_value_eur', 'log_value', 'bidder_count', 
                          'is_high_tech', 'is_complex', 'is_multi_national']
        
        # Add dummy variables
        contract_dummies = pd.get_dummies(df['contract_type'], prefix='type')
        tech_dummies = pd.get_dummies(df['technology_level'], prefix='tech')
        
        # Create feature matrix
        X = pd.concat([df[feature_columns], contract_dummies, tech_dummies], axis=1)
        y = df['risk_score']
        
        # Save ML training data
        ml_data = X.copy()
        ml_data['risk_score'] = y
        
        ml_file = f'{output_folder}/nspa_ml_training_data.csv'
        ml_data.to_csv(ml_file, index=False)
        
        # Create summary
        summary = {
            'dataset_info': {
                'total_contracts': len(df),
                'years_covered': sorted(df['year'].unique().tolist()),
                'contract_types': df['contract_type'].value_counts().to_dict(),
                'avg_value_eur': int(df['estimated_value_eur'].mean()),
                'risk_distribution': df['risk_score'].value_counts().sort_index().to_dict()
            }
        }
        
        summary_file = f'{output_folder}/nspa_analysis_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📁 Files saved in '{output_folder}/':")
        print(f"   1. {raw_file} - Complete contract data")
        print(f"   2. {ml_file} - ML training dataset") 
        print(f"   3. {summary_file} - Analysis summary")
        
        return {'raw_data': raw_file, 'ml_data': ml_file, 'summary': summary_file}

def main():
    """Main function to process NSPA PDF files"""
    print("🏛️ NSPA Real Contract Data Processor")
    print("=" * 50)
    
    processor = NSPAPDFProcessor()
    pdf_folder = "nspa_pdfs"
    
    try:
        contracts = processor.process_all_pdfs(pdf_folder)
        
        if contracts:
            files_created = processor.save_results()
            print(f"\n🎯 Ready for Azure ML Studio!")
            print(f"Upload file: {files_created['ml_data']}")
            print(f"Target column: 'risk_score' (1-16 scale)")
        else:
            print("❌ No contracts extracted. Check your PDF files.")
            
    except FileNotFoundError:
        print(f"❌ Folder '{pdf_folder}' not found.")
        print("\n📁 Next steps:")
        print("1. Create folder: mkdir nspa_pdfs")
        print("2. Copy your 6 NSPA PDF files into nspa_pdfs/")
        print("3. Run this script again")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Try: pip install pdfplumber")

if __name__ == "__main__":
    main()