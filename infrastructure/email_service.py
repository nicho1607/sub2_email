import smtplib
from email.mime.text import MIMEText
from config.email_config import EmailConfig

class EmailService:
    def __init__(self):
        self.config = EmailConfig()
    
    def send_email(self, body):
        try:
            msg = MIMEText(body)
            msg['Subject'] = self.config.email_subject
            msg['From'] = self.config.email_from
            msg['To'] = self.config.email_to
            
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.starttls()
                server.login(self.config.email_from, self.config.email_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error enviando email: {str(e)}")
            return False