"""
Data Export Service - Generate downloadable reports in PDF, CSV, and JSON formats
"""

from typing import Dict, List
from datetime import datetime
import json
import pandas as pd
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class DataExportService:
    """Generate downloadable intelligence reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom PDF styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2d3748'),
            spaceAfter=12,
            spaceBefore=12
        ))
    
    def generate_pdf_report(self, report_data: Dict) -> BytesIO:
        """
        Generate professional PDF intelligence report
        
        Args:
            report_data: Complete intelligence report data
        
        Returns:
            BytesIO: PDF file in memory
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        story = []
        
        # Title
        title = Paragraph("🛡️ ScamShield Intelligence Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Metadata
        metadata = [
            ['Report ID:', report_data.get('conversation_id', 'N/A')],
            ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Scam Type:', report_data.get('scam_type', 'Unknown')],
            ['Risk Score:', f"{report_data.get('risk_score', 0) * 100:.0f}%"]
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2d3748')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0'))
        ]))
        story.append(metadata_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Summary
        story.append(Paragraph("Conversation Summary", self.styles['CustomHeading']))
        summary_text = report_data.get('conversation_summary', 'No summary available')
        story.append(Paragraph(summary_text, self.styles['BodyText']))
        story.append(Spacer(1, 0.2*inch))
        
        # Red Flags
        story.append(Paragraph("🚩 Red Flags Identified", self.styles['CustomHeading']))
        red_flags = report_data.get('red_flags', [])
        for flag in red_flags:
            story.append(Paragraph(f"• {flag}", self.styles['BodyText']))
        story.append(Spacer(1, 0.2*inch))
        
        # Extracted Entities
        story.append(Paragraph("📊 Extracted Intelligence", self.styles['CustomHeading']))
        entities = report_data.get('extracted_entities', {})
        
        entity_data = []
        entity_data.append(['Category', 'Details'])
        
        if entities.get('upi_ids'):
            entity_data.append(['UPI IDs', ', '.join(entities['upi_ids'])])
        
        if entities.get('bank_accounts'):
            accounts = [f"{acc.get('account_number', 'N/A')} ({acc.get('ifsc', 'N/A')})" 
                       for acc in entities['bank_accounts']]
            entity_data.append(['Bank Accounts', ', '.join(accounts)])
        
        if entities.get('phone_numbers'):
            entity_data.append(['Phone Numbers', ', '.join(entities['phone_numbers'])])
        
        if entities.get('phishing_links'):
            entity_data.append(['Phishing Links', ', '.join(entities['phishing_links'])])
        
        if len(entity_data) > 1:
            entity_table = Table(entity_data, colWidths=[2*inch, 4*inch])
            entity_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')])
            ]))
            story.append(entity_table)
        else:
            story.append(Paragraph("No entities extracted", self.styles['BodyText']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Recommended Actions
        story.append(Paragraph("✅ Recommended Actions", self.styles['CustomHeading']))
        actions = report_data.get('recommended_actions', [])
        for i, action in enumerate(actions, 1):
            story.append(Paragraph(f"{i}. {action}", self.styles['BodyText']))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(
            "ScamShield AI - Making India Safer 🇮🇳<br/>India AI Impact Buildathon 2026",
            self.styles['BodyText']
        )
        story.append(footer)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_csv_export(self, conversations: List[Dict]) -> BytesIO:
        """
        Generate CSV export of multiple conversations
        
        Args:
            conversations: List of conversation data
        
        Returns:
            BytesIO: CSV file in memory
        """
        # Flatten conversation data for CSV
        rows = []
        for conv in conversations:
            row = {
                'Conversation ID': conv.get('conversation_id', ''),
                'Timestamp': conv.get('timestamp', ''),
                'Scam Type': conv.get('scam_type', ''),
                'Risk Score': conv.get('risk_score', 0),
                'Confidence': conv.get('confidence_level', ''),
                'Turn Number': conv.get('turn_number', 0),
                'Scammer Message': conv.get('scammer_message', ''),
                'Agent Response': conv.get('agent_response', ''),
                'UPI IDs': ', '.join(conv.get('extracted_entities', {}).get('upi_ids', [])),
                'Phone Numbers': ', '.join(conv.get('extracted_entities', {}).get('phone_numbers', [])),
                'Phishing Links': ', '.join(conv.get('extracted_entities', {}).get('phishing_links', []))
            }
            rows.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(rows)
        
        # Export to CSV
        buffer = BytesIO()
        df.to_csv(buffer, index=False, encoding='utf-8')
        buffer.seek(0)
        return buffer
    
    def generate_json_export(self, report_data: Dict) -> str:
        """
        Generate structured JSON export
        
        Args:
            report_data: Intelligence report data
        
        Returns:
            str: Formatted JSON string
        """
        # Add metadata
        export_data = {
            'export_metadata': {
                'generated_at': datetime.now().isoformat(),
                'format_version': '1.0',
                'source': 'ScamShield AI'
            },
            'report': report_data
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def generate_excel_export(self, conversations: List[Dict]) -> BytesIO:
        """
        Generate Excel export with multiple sheets
        
        Args:
            conversations: List of conversation data
        
        Returns:
            BytesIO: Excel file in memory
        """
        buffer = BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = []
            for conv in conversations:
                summary_data.append({
                    'ID': conv.get('conversation_id', ''),
                    'Date': conv.get('timestamp', ''),
                    'Scam Type': conv.get('scam_type', ''),
                    'Risk Score': conv.get('risk_score', 0),
                    'Turns': conv.get('turn_number', 0)
                })
            
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Entities sheet
            entity_data = []
            for conv in conversations:
                entities = conv.get('extracted_entities', {})
                entity_data.append({
                    'Conversation ID': conv.get('conversation_id', ''),
                    'UPI IDs': ', '.join(entities.get('upi_ids', [])),
                    'Phone Numbers': ', '.join(entities.get('phone_numbers', [])),
                    'Bank Accounts': ', '.join([acc.get('account_number', '') for acc in entities.get('bank_accounts', [])]),
                    'Phishing Links': ', '.join(entities.get('phishing_links', []))
                })
            
            df_entities = pd.DataFrame(entity_data)
            df_entities.to_excel(writer, sheet_name='Extracted Entities', index=False)
        
        buffer.seek(0)
        return buffer


# Singleton instance
data_export_service = DataExportService()
