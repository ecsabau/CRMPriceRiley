from typing import Dict
import re
from .database import CRMDB
import logging

class LeadScorer:
    def __init__(self, db: CRMDB):
        self.db = db
        self.logger = logging.getLogger(__name__)
        
    def calculate_score(self, lead_data: Dict) -> int:
        """Calculate AI-based lead score (0-100)"""
        try:
            base = 0
            
            # Email domain analysis
            if self._is_property_related(lead_data.get('email', '')):
                base += 30
                
            # Source analysis
            if lead_data.get('source') == 'website_form':
                base += 20
            elif lead_data.get('source') == 'meta':
                base += 15
            elif lead_data.get('source') == 'ga':
                base += 10
                
            # Engagement metrics (simplified example)
            engagement = self._estimate_engagement(lead_data)
            base += engagement
            
            # Ensure score is within bounds
            return max(0, min(100, base))
            
        except Exception as e:
            self.logger.error(f"Error calculating lead score: {e}")
            return 0
    
    def _is_property_related(self, email: str) -> bool:
        """Check if email suggests property interest"""
        property_keywords = ['property', 'realestate', 'invest', 'landlord']
        domain = email.split('@')[-1].lower()
        return any(keyword in domain for keyword in property_keywords)
    
    def _estimate_engagement(self, lead_data: Dict) -> int:
        """Estimate engagement score based on available data"""
        engagement = 0
        
        # Phone number presence
        if lead_data.get('phone'):
            engagement += 10
            
        # Name completeness
        if ' ' in lead_data.get('name', ''):
            engagement += 5
            
        return engagement
    
    def auto_tag_lead(self, lead_data: Dict) -> str:
        """Generate automatic tags for lead"""
        tags = []
        
        if self._is_property_related(lead_data.get('email', '')):
            tags.append('UK Property Investor')
            
        if lead_data.get('source') == 'website_form':
            tags.append('High Intent')
            
        return ', '.join(tags)
    
    def process_new_lead(self, lead_data: Dict) -> int:
        """Full processing pipeline for new lead"""
        # Calculate score
        lead_data['score'] = self.calculate_score(lead_data)
        
        # Auto-tagging
        lead_data['tags'] = self.auto_tag_lead(lead_data)
        
        # Save to database
        return self.db.add_lead(lead_data)