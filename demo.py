# /investor_ai_crm/crm/demo.py
from flask import Blueprint, render_template_string, send_from_directory
from datetime import datetime
import os
from fpdf import FPDF

# Create blueprint
demo_bp = Blueprint('demo', __name__, url_prefix='/demo')

# Demo Templates
DEMO_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>PriceRiley CRM Demo</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .report { border: 1px solid #eee; padding: 20px; margin-top: 20px; }
        .qualified { color: #27ae60; }
        .contacted { color: #f39c12; }
        .new { color: #3498db; }
    </style>
</head>
<body>
    <h1>CRM Demo Mode</h1>
    <div class="report">
        <h2>INVESTOR ANALYTICS REPORT</h2>
        <p><strong>Generated:</strong> {{ timestamp }}</p>
        <ul>
            <li>• Alex Johnson: Score 0.92 <span class="qualified">(Qualified)</span></li>
            <li>• Taylor Smith: Score 0.85 <span class="contacted">(Contacted)</span></li>
            <li>• Sam Lee: Score 0.78 <span class="new">(New)</span></li>
        </ul>
    </div>
</body>
</html>
"""

@demo_bp.route('/')
def demo_hub():
    return render_template_string(DEMO_HTML, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M'))

@demo_bp.route('/pdf')
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="INVESTOR ANALYTICS REPORT", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
    pdf.cell(200, 10, txt="- Alex Johnson: Score 0.92 (Qualified)", ln=1)
    pdf.cell(200, 10, txt="- Taylor Smith: Score 0.85 (Contacted)", ln=1)
    pdf.cell(200, 10, txt="- Sam Lee: Score 0.78 (New)", ln=1)
    
    os.makedirs('output/reports', exist_ok=True)
    filename = f"demo_report_{datetime.now().strftime('%Y%m%d')}.pdf"
    filepath = os.path.join('output/reports', filename)
    pdf.output(filepath)
    
    return send_from_directory('output/reports', filename, as_attachment=True)

def register_demo(app):
    """Safe registration function"""
    app.register_blueprint(demo_bp)
    print("Demo routes registered at /demo")
    return app