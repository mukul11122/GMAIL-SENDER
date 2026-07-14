import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
import os
from config import EMAIL_SETTINGS

class GmailService:
    def __init__(self):
        self.smtp_server = EMAIL_SETTINGS['smtp_server']
        self.smtp_port = EMAIL_SETTINGS['smtp_port']
        self.delay_between_emails = EMAIL_SETTINGS['delay_between_emails']
        self.delay_between_batches = EMAIL_SETTINGS['delay_between_batches']
        self.batch_size = EMAIL_SETTINGS['batch_size']
    
    def send_email(self, recipient_email, subject, html_content, sender_email, sender_password, attachment_path=None):
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        if attachment_path and os.path.exists(attachment_path):
            try:
                with open(attachment_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                
                encoders.encode_base64(part)
                filename = os.path.basename(attachment_path)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{filename}"'
                )
                msg.attach(part)
            except Exception as e:
                return False, f"Attachment error: {str(e)}"
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                return True, "Sent successfully"
        except smtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Check email/password (use App Password)"
        except smtplib.SMTPException as e:
            return False, f"SMTP error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def send_batch(self, customers, subject, html_content, gmail_account, progress_callback=None, attachment_path=None):
        account_id, sender_email, sender_password = gmail_account
        
        results = {
            'sent': 0,
            'failed': 0,
            'errors': []
        }
        
        for i, customer in enumerate(customers):
            customer_id, email, store_code, mobile_number = customer[0], customer[1], customer[2], customer[3]
            
            personalized_html = html_content.replace('{{name}}', store_code or 'Customer')
            personalized_html = personalized_html.replace('{{email}}', email)
            
            success, message = self.send_email(email, subject, personalized_html, sender_email, sender_password, attachment_path)
            
            if success:
                results['sent'] += 1
                yield (customer_id, 'sent', sender_email)
            else:
                results['failed'] += 1
                results['errors'].append(f"{email}: {message}")
                yield (customer_id, 'failed', sender_email)
            
            if progress_callback:
                progress_callback(i + 1, len(customers))
            
            if i < len(customers) - 1:
                time.sleep(self.delay_between_emails)
        
        return results
