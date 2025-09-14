# crm_dashboard.py
from flask import Flask, render_template
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    try:
        with open('website_scan.json') as f:
            scan_data = json.load(f)
    except FileNotFoundError:
        scan_data = {"error": "No scan data available"}
    
    return render_template('dashboard.html', 
                         scan_data=scan_data,
                         current_time=datetime.now())

if __name__ == '__main__':
    app.run(port=5001)  # Different port from your main app