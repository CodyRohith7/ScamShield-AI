"""
Email Service - Send intelligence reports to owner and cybercrime authorities
"""

import os
from typing import List, Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime
import json


class EmailService:
    """Handle email notifications for ScamShield AI"""
    
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("FROM_EMAIL", "scamshield@example.com")
        self.owner_email = os.getenv("OWNER_EMAIL")
        self.cybercrime_email = os.getenv("CYBERCRIME_EMAIL", "cybercrime@gov.in")
        
        self.enabled = bool(self.api_key)
        if not self.enabled:
            print("WARNING: Email service disabled: SENDGRID_API_KEY not configured")
    
    async def send_intelligence_report(
        self,
        conversation_id: str,
        report_data: dict,
        recipients: List[str] = None
    ) -> bool:
        """
        Send intelligence report via email
        
        Args:
            conversation_id: Unique conversation identifier
            report_data: Complete intelligence report
            recipients: List of email addresses (defaults to owner + cybercrime)
        
        Returns:
            bool: True if sent successfully
        """
        if not self.enabled:
            print("📧 Email service not configured, skipping...")
            return False
        
        if recipients is None:
            recipients = [self.owner_email, self.cybercrime_email]
            recipients = [r for r in recipients if r]  # Remove None values
        
        if not recipients:
            print("⚠️  No recipients configured")
            return False
        
        try:
            # Create email content
            subject = f"🚨 ScamShield Alert: {report_data.get('scam_type', 'Unknown')} Detected"
            html_content = self._generate_html_report(conversation_id, report_data)
            
            message = Mail(
                from_email=self.from_email,
                to_emails=recipients,
                subject=subject,
                html_content=html_content
            )
            
            # Send email
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            print(f"✅ Email sent successfully (Status: {response.status_code})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False
    
    async def send_high_risk_alert(
        self,
        conversation_id: str,
        risk_score: float,
        extracted_entities: dict
    ) -> bool:
        """Send immediate alert for high-risk scams"""
        if not self.enabled or risk_score < 0.8:
            return False
        
        try:
            subject = f"🚨 HIGH RISK SCAM DETECTED - Immediate Action Required"
            
            html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                        <h1 style="color: white; margin: 0;">⚠️ HIGH RISK ALERT</h1>
                    </div>
                    
                    <div style="padding: 30px; background: #f7fafc;">
                        <h2 style="color: #2d3748;">Scam Detection Alert</h2>
                        
                        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                            <p><strong>Conversation ID:</strong> {conversation_id}</p>
                            <p><strong>Risk Score:</strong> <span style="color: #e53e3e; font-size: 24px; font-weight: bold;">{risk_score * 100:.0f}%</span></p>
                            <p><strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        </div>
                        
                        <h3 style="color: #2d3748;">Extracted Intelligence:</h3>
                        <div style="background: white; padding: 20px; border-radius: 8px;">
                            <pre style="background: #edf2f7; padding: 15px; border-radius: 4px; overflow-x: auto;">
{json.dumps(extracted_entities, indent=2)}
                            </pre>
                        </div>
                        
                        <div style="margin-top: 30px; padding: 20px; background: #fff5f5; border-left: 4px solid #e53e3e; border-radius: 4px;">
                            <p style="margin: 0; color: #742a2a;"><strong>⚡ Immediate Action Required</strong></p>
                            <p style="margin: 10px 0 0 0; color: #742a2a;">This scam attempt has been flagged as high-risk. Please review and take appropriate action.</p>
                        </div>
                    </div>
                    
                    <div style="padding: 20px; text-align: center; color: #718096; font-size: 12px;">
                        <p>ScamShield AI - Making India Safer 🇮🇳</p>
                        <p>India AI Impact Buildathon 2026</p>
                    </div>
                </body>
            </html>
            """
            
            message = Mail(
                from_email=self.from_email,
                to_emails=[self.owner_email] if self.owner_email else [],
                subject=subject,
                html_content=html_content
            )
            
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            print(f"🚨 High-risk alert sent (Status: {response.status_code})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send high-risk alert: {str(e)}")
            return False
    
    def _generate_html_report(self, conversation_id: str, report_data: dict) -> str:
        """Generate beautiful HTML email report"""
        
        extracted = report_data.get('extracted_entities', {})
        
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f7fafc;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                    <h1 style="color: white; margin: 0;">🛡️ ScamShield Intelligence Report</h1>
                </div>
                
                <div style="padding: 30px;">
                    <div style="background: white; padding: 25px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h2 style="color: #2d3748; margin-top: 0;">Conversation Summary</h2>
                        <p style="color: #4a5568; line-height: 1.6;">{report_data.get('conversation_summary', 'N/A')}</p>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px;">
                            <div style="background: #edf2f7; padding: 15px; border-radius: 6px;">
                                <div style="color: #718096; font-size: 12px; margin-bottom: 5px;">Scam Type</div>
                                <div style="color: #2d3748; font-weight: bold;">{report_data.get('scam_type', 'Unknown')}</div>
                            </div>
                            <div style="background: #edf2f7; padding: 15px; border-radius: 6px;">
                                <div style="color: #718096; font-size: 12px; margin-bottom: 5px;">Risk Score</div>
                                <div style="color: #e53e3e; font-weight: bold; font-size: 20px;">{report_data.get('risk_score', 0) * 100:.0f}%</div>
                            </div>
                        </div>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h3 style="color: #2d3748; margin-top: 0;">🚩 Red Flags Identified</h3>
                        <ul style="color: #4a5568; line-height: 1.8;">
                            {''.join([f'<li>{flag}</li>' for flag in report_data.get('red_flags', [])])}
                        </ul>
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h3 style="color: #2d3748; margin-top: 0;">📊 Extracted Intelligence</h3>
                        
                        {self._format_entities_html(extracted)}
                    </div>
                    
                    <div style="background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h3 style="color: #2d3748; margin-top: 0;">✅ Recommended Actions</h3>
                        <ol style="color: #4a5568; line-height: 1.8;">
                            {''.join([f'<li>{action}</li>' for action in report_data.get('recommended_actions', [])])}
                        </ol>
                    </div>
                </div>
                
                <div style="padding: 20px; text-align: center; color: #718096; font-size: 12px;">
                    <p>Report ID: {conversation_id}</p>
                    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p style="margin-top: 20px;">ScamShield AI - Making India Safer 🇮🇳</p>
                </div>
            </body>
        </html>
        """
    
    def _format_entities_html(self, entities: dict) -> str:
        """Format extracted entities as HTML"""
        html_parts = []
        
        entity_icons = {
            'upi_ids': '💳',
            'bank_accounts': '🏦',
            'phone_numbers': '📞',
            'phishing_links': '🔗',
            'aliases': '👤',
            'fake_organizations': '🏢'
        }
        
        for key, icon in entity_icons.items():
            items = entities.get(key, [])
            if items:
                if key == 'bank_accounts':
                    items = [f"{acc.get('account_number', 'N/A')} ({acc.get('ifsc', 'N/A')})" for acc in items]
                
                html_parts.append(f"""
                <div style="margin-bottom: 15px;">
                    <div style="color: #2d3748; font-weight: bold; margin-bottom: 8px;">{icon} {key.replace('_', ' ').title()}</div>
                    <div style="background: #edf2f7; padding: 12px; border-radius: 4px;">
                        {'<br>'.join([f'<code style="background: white; padding: 4px 8px; border-radius: 3px; font-size: 13px;">{item}</code>' for item in items])}
                    </div>
                </div>
                """)
        
        return ''.join(html_parts) if html_parts else '<p style="color: #718096;">No entities extracted</p>'


# Singleton instance
email_service = EmailService()
