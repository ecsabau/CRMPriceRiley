from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    Filter,
    FilterExpression
)
import logging
from typing import List, Dict

class GA4Connector:
    def __init__(self, property_id: str, credentials_path: str = None):
        self.property_id = property_id
        self.credentials_path = credentials_path
        self.client = self._initialize_client()
        self.logger = logging.getLogger(__name__)
        
    def _initialize_client(self):
        """Initialize GA4 client with optional credentials"""
        if self.credentials_path:
            return BetaAnalyticsDataClient.from_service_account_json(self.credentials_path)
        return BetaAnalyticsDataClient()
    
    def get_investor_leads(self, days: int = 7) -> List[Dict]:
        """Get investor page leads from GA4"""
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[Dimension(name="pagePath")],
                metrics=[Metric(name="sessions")],
                date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
                dimension_filter=FilterExpression(
                    filter=Filter(
                        field_name="pagePath",
                        string_filter=Filter.StringFilter(match_type="CONTAINS", value="/investors")
                    )
                )
            )
            
            response = self.client.run_report(request)
            
            results = []
            for row in response.rows:
                results.append({
                    'page_path': row.dimension_values[0].value,
                    'sessions': row.metric_values[0].value
                })
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error fetching GA4 data: {e}")
            return []
    
    def get_top_converting_pages(self, days: int = 30, limit: int = 10) -> List[Dict]:
        """Get top converting pages with conversion rates"""
        try:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[Dimension(name="pagePath")],
                metrics=[
                    Metric(name="sessions"),
                    Metric(name="conversions")
                ],
                date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
                limit=limit,
                order_bys=["metrics.conversions desc"]
            )
            
            response = self.client.run_report(request)
            
            results = []
            for row in response.rows:
                sessions = int(row.metric_values[0].value)
                conversions = int(row.metric_values[1].value)
                conversion_rate = (conversions / sessions * 100) if sessions > 0 else 0
                
                results.append({
                    'page_path': row.dimension_values[0].value,
                    'sessions': sessions,
                    'conversions': conversions,
                    'conversion_rate': round(conversion_rate, 2)
                })
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error fetching conversion data: {e}")
            return []