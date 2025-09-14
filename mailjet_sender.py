import os
from mailjet_rest import Client
from typing import Dict, List, Optional
import logging

class MailjetEmailer:
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or os.getenv('MAILJET_API_KEY')
        self.api_secret = api_secret or os.getenv('MAILJET_API_SECRET')
        self.client = Client(auth=(self.api_key, self.api_secret))
        self.logger = logging.getLogger(__name__)
        
    def send_transactional_email(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        html_content: str,
        template_id: Optional[int] = None,
        variables: Optional[Dict] = None
    ) -> bool:
        """Send a transactional email via Mailjet"""
        try:
            data = {
                'Messages': [{
                    'From': {
                        'Email': 'noreply@priceriley.co.uk',
                        'Name': 'PriceRiley CRM'
                    },
                    'To': [{
                        'Email': to_email,
                        'Name': to_name
                    }],
                    'Subject': subject,
                    'HTMLPart': html_content
                }]
            }
            
            if template_id:
                data['Messages'][0]['TemplateID'] = template_id
                data['Messages'][0]['TemplateLanguage'] = True
                
            if variables:
                data['Messages'][0]['Variables'] = variables
                
            result = self.client.send.create(data=data)
            return result.status_code == 200
            
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False
    
    def send_lead_notification(self, lead_data: Dict) -> bool:
        """Send notification about a new high-value lead"""
        if lead_data.get('score', 0) < 70:  # Only notify for high-value leads
            return False
            
        subject = f"New High-Value Lead: {lead_data.get('name')}"
        html_content = f"""
        <h3>New High-Value Lead</h3>
        <p><strong>Name:</strong> {lead_data.get('name')}</p>
        <p><strong>Email:</strong> {lead_data.get('email')}</p>
        <p><strong>Phone:</strong> {lead_data.get('phone', 'Not provided')}</p>
        <p><strong>Score:</strong> {lead_data.get('score')}/100</p>
        <p><strong>Source:</strong> {lead_data.get('source', 'Unknown')}</p>
        """
        
        # Send to sales team
        return self.send_transactional_email(
            to_email='sales@priceriley.co.uk',
            to_name='Sales Team',
            subject=subject,
            html_content=html_content
        )