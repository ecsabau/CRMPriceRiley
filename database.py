import sqlite3
from datetime import datetime
import csv
from fpdf import FPDF
from typing import List, Dict, Optional

class CRMDB:
    def __init__(self, db_path: str = 'leads.db'):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
        
    def _create_tables(self):
        """Initialize database tables"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                status TEXT CHECK(status IN ('new', 'contacted', 'qualified')) DEFAULT 'new',
                score INTEGER DEFAULT 0,
                source TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                tags TEXT
            )
        ''')
        self.conn.commit()
        
    def add_lead(self, lead_data: Dict) -> int:
        """Insert a new lead into the database"""
        required_fields = ['name', 'email']
        if not all(field in lead_data for field in required_fields):
            raise ValueError("Missing required lead fields")
            
        query = '''
            INSERT INTO leads (name, email, phone, status, score, source, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                name=excluded.name,
                phone=excluded.phone,
                status=excluded.status,
                score=excluded.score,
                source=excluded.source,
                tags=excluded.tags
        '''
        values = (
            lead_data['name'],
            lead_data['email'],
            lead_data.get('phone', ''),
            lead_data.get('status', 'new'),
            lead_data.get('score', 0),
            lead_data.get('source', ''),
            lead_data.get('tags', '')
        )
        
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        self.conn.commit()
        return cursor.lastrowid
    
    def update_lead_status(self, lead_id: int, new_status: str) -> bool:
        """Update a lead's status with validation"""
        valid_statuses = ['new', 'contacted', 'qualified']
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE leads SET status = ? WHERE id = ?
        ''', (new_status, lead_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_leads(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Retrieve leads with optional filtering"""
        base_query = 'SELECT * FROM leads'
        params = []
        conditions = []
        
        if filters:
            if 'status' in filters:
                conditions.append('status = ?')
                params.append(filters['status'])
            if 'min_score' in filters:
                conditions.append('score >= ?')
                params.append(filters['min_score'])
            if 'max_score' in filters:
                conditions.append('score <= ?')
                params.append(filters['max_score'])
            if 'source' in filters:
                conditions.append('source = ?')
                params.append(filters['source'])
                
        if conditions:
            base_query += ' WHERE ' + ' AND '.join(conditions)
            
        cursor = self.conn.cursor()
        cursor.execute(base_query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def generate_daily_report(self, report_format: str = 'csv') -> str:
        """Generate daily lead report in CSV or PDF format"""
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f"leads_report_{today}.{report_format.lower()}"
        leads = self.get_leads()
        
        if report_format.lower() == 'csv':
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=leads[0].keys())
                writer.writeheader()
                writer.writerows(leads)
        elif report_format.lower() == 'pdf':
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            # Report title
            pdf.cell(200, 10, txt=f"Daily Leads Report - {today}", ln=1, align='C')
            
            # Table header
            pdf.set_font("Arial", 'B', 10)
            headers = ['ID', 'Name', 'Email', 'Status', 'Score']
            col_widths = [15, 40, 70, 30, 20]
            
            for header, width in zip(headers, col_widths):
                pdf.cell(width, 10, txt=header, border=1)
            pdf.ln()
            
            # Table rows
            pdf.set_font("Arial", size=10)
            for lead in leads:
                pdf.cell(col_widths[0], 10, txt=str(lead['id']), border=1)
                pdf.cell(col_widths[1], 10, txt=lead['name'], border=1)
                pdf.cell(col_widths[2], 10, txt=lead['email'], border=1)
                pdf.cell(col_widths[3], 10, txt=lead['status'], border=1)
                pdf.cell(col_widths[4], 10, txt=str(lead['score']), border=1)
                pdf.ln()
            
            pdf.output(filename)
        else:
            raise ValueError("Unsupported report format. Use 'csv' or 'pdf'")
            
        return filename
    
    def backup_database(self, backup_path: str = 'backups/'):
        """Create a timestamped database backup"""
        import os
        import shutil
        from datetime import datetime
        
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_path, f'leads_backup_{timestamp}.db')
        shutil.copy2('leads.db', backup_file)
        return backup_file
    
    def __del__(self):
        """Clean up database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()