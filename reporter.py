from fpdf import FPDF
import csv
import json
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self):
        os.makedirs("output/reports", exist_ok=True)
    
    def generate_pdf(self, data, filename="investor_report"):
        """Generate PDF report"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Title
        pdf.cell(200, 10, txt="PriceRiley Investor Report", ln=1, align='C')
        pdf.ln(10)
        
        # Content
        for lead in data:
            pdf.cell(200, 10, txt=f"Name: {lead['name']}", ln=1)
            pdf.cell(200, 10, txt=f"Email: {lead['email']}", ln=1)
            pdf.cell(200, 10, txt=f"Score: {lead['score']}", ln=1)
            pdf.ln(5)
        
        pdf.output(f"output/reports/{filename}_{datetime.now().strftime('%Y%m%d')}.pdf")
    
    def generate_csv(self, data, filename="investor_report"):
        """Generate CSV report"""
        with open(f"output/reports/{filename}_{datetime.now().strftime('%Y%m%d')}.csv", 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    def generate_json(self, data, filename="investor_report"):
        """Generate JSON report"""
        with open(f"output/reports/{filename}_{datetime.now().strftime('%Y%m%d')}.json", 'w') as file:
            json.dump(data, file, indent=4)