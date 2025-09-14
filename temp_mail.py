import logging
import smtplib
from email.mime.text import MIMEText
from typing import Optional

logger = logging.getLogger("PriceRileyAI")

class TempMailSender:
    """
    Fallback email sender using SMTP (for testing when Mailjet fails).
    Uses a local SMTP server or Gmail's SMTP with app passwords.
    """
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "your-test-email@gmail.com"  # Replace with your test email
        self.sender_password = "your-app-password"      # Gmail app password (NOT main password)

    def send_email(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """
        Send email via SMTP fallback.
        
        Args:
            recipient_email: Target email address
            subject: Email subject
            body: Plaintext email content
            html_body: Optional HTML content
            
        Returns:
            bool: True if sent successfully
        """
        try:
            msg = MIMEText(html_body if html_body else body, "html" if html_body else "plain")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"TempMail: Email sent to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"TempMail failed: {str(e)}")
            return False