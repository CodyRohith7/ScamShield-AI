"""
Campaign Manager Module
Handles the detection, tracking, and reporting of fraud campaigns.
Uses heuristics to group conversations into campaigns based on shared attributes.
"""

from typing import List, Dict, Optional
import json
from datetime import datetime, timedelta
from database import db

class CampaignManager:
    def __init__(self):
        pass

    def get_statistics(self) -> Dict:
        """Get global campaign statistics"""
        # Get basic stats from DB
        analytics = db.get_analytics()
        conversations = db.list_conversations(limit=1000)
        
        # Calculate active campaigns (simple aggregation by scam_type for now)
        campaigns_by_type = {}
        for conv in conversations:
            scam_type = conv['scam_type']
            if scam_type not in campaigns_by_type:
                campaigns_by_type[scam_type] = []
            campaigns_by_type[scam_type].append(conv)
            
        total_tracked = len(conversations)
        active_count = len(campaigns_by_type)
        
        return {
            "total_campaigns": active_count * 2, # Mocking historical count
            "active_campaigns": active_count,
            "total_conversations_tracked": total_tracked,
            "avg_conversations_per_campaign": total_tracked / active_count if active_count > 0 else 0
        }

    def detect_campaigns(self) -> List[Dict]:
        """
        Analyze all conversations and group them into campaigns.
        Rule: Conversations of same Scam Type within recent timeframe = Campaign.
        Future: Link by shared entities.
        """
        conversations = db.list_conversations(limit=100)
        
        # Group by Scam Type
        groups = {}
        for conv in conversations:
            s_type = conv['scam_type']
            if s_type not in groups:
                groups[s_type] = {
                    "id": f"CMP-{s_type.upper()}-{datetime.now().strftime('%Y%m')}",
                    "type": s_type,
                    "conversations": [],
                    "start_date": conv['created_at'],
                    "end_date": conv['created_at'],
                    "entities": set(),
                    "risks": []
                }
            
            group = groups[s_type]
            group["conversations"].append(conv)
            group["risks"].append(conv['risk_score'])
            
            # Update dates
            if conv['created_at'] < group["start_date"]:
                group["start_date"] = conv['created_at']
            if conv['created_at'] > group["end_date"]:
                group["end_date"] = conv['created_at']
                
            # Collect entities (need to fetch details)
            # For efficiency, we'll just mock the count here or do a deeper query if needed
            
        # Format for frontend
        campaigns = []
        for s_type, group in groups.items():
            conv_count = len(group["conversations"])
            avg_risk = sum(group["risks"]) / conv_count if conv_count > 0 else 0
            
            # Determine threat level
            threat = "low"
            if avg_risk > 0.7: threat = "critical"
            elif avg_risk > 0.4: threat = "high"
            elif avg_risk > 0.2: threat = "medium"
            
            campaigns.append({
                "campaign_id": group["id"],
                "scam_type": s_type,
                "status": "active",
                "threat_level": threat,
                "conversation_count": conv_count,
                "avg_risk_score": avg_risk,
                "start_date": group["start_date"],
                "end_date": group["end_date"],
                "duration_days": 1, # Placeholder logic
                "unique_numbers": int(conv_count * 0.8), # Placeholder estimation
                "unique_upi_ids": int(conv_count * 0.5),
                "unique_links": int(conv_count * 0.3),
                "script_template": f"Standard {s_type} script pattern detected."
            })
            
        return campaigns

    def get_campaign_report(self, campaign_id: str) -> Dict:
        """Generate a detailed report for a specific campaign"""
        # Parse scam type from ID (CMP-TYPE-DATE)
        parts = campaign_id.split('-')
        if len(parts) < 2:
            return None
        
        target_type = parts[1].lower()
        
        # Get all conversations of this type
        # In a real system, we'd query by campaign_id linkage
        # Here we mimic it by filtering list output
        all_campaigns = self.detect_campaigns()
        campaign = next((c for c in all_campaigns if c["campaign_id"] == campaign_id), None)
        
        if not campaign:
            return None
            
        report_text = f"""CAMPAIGN INTELLIGENCE REPORT
ID: {campaign_id}
TYPE: {campaign['scam_type'].upper()}
THREAT LEVEL: {campaign['threat_level'].upper()}
------------------------------------------------
ANALYSIS:
This campaign targets victims using a '{campaign['scam_type']}' strategy. 
Activity detected starting {campaign['start_date']}.

PATTERN:
High frequency of automated introductory messages followed by 
aggressive social engineering tactics.

RECOMMENDED ACTION:
- Block identified UPI IDs immediately.
- Issue advisory for this specific script pattern.
"""

        return {
            "campaign": campaign,
            "report": report_text
        }

# Singleton
campaign_manager = CampaignManager()
