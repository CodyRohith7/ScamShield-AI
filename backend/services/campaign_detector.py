"""
Campaign Detection - Identify and track fraud campaigns across conversations
"""

import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity


class CampaignDetector:
    """Detect and track fraud campaigns across multiple conversations"""
    
    def __init__(self):
        self.campaigns = {}
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    
    def detect_campaigns(self, conversations: List[Dict], 
                        similarity_threshold: float = 0.7,
                        min_conversations: int = 2) -> List[Dict]:
        """
        Detect campaigns from a list of conversations
        
        Args:
            conversations: List of conversation dictionaries
            similarity_threshold: Minimum similarity to group conversations
            min_conversations: Minimum conversations to form a campaign
        
        Returns:
            List of detected campaigns with metadata
        """
        if len(conversations) < min_conversations:
            return []
        
        # Extract features from each conversation
        features = self._extract_features_batch(conversations)
        
        # Cluster similar conversations
        clusters = self._cluster_conversations(features, similarity_threshold, min_conversations)
        
        # Analyze each cluster as a campaign
        campaigns = []
        for cluster_id, conv_indices in clusters.items():
            if len(conv_indices) >= min_conversations:
                campaign = self._analyze_campaign(
                    [conversations[i] for i in conv_indices],
                    cluster_id
                )
                campaigns.append(campaign)
        
        # Store campaigns
        for campaign in campaigns:
            self.campaigns[campaign['campaign_id']] = campaign
        
        return campaigns
    
    def _extract_features_batch(self, conversations: List[Dict]) -> np.ndarray:
        """Extract features from multiple conversations for clustering"""
        
        feature_vectors = []
        
        for conv in conversations:
            features = self._extract_campaign_features(conv)
            feature_vectors.append(features)
        
        return np.array(feature_vectors)
    
    def _extract_campaign_features(self, conversation: Dict) -> np.ndarray:
        """
        Extract features for campaign detection
        
        Features:
        - Scam type encoding
        - Key phrase TF-IDF
        - Entity pattern similarity
        - Timing patterns
        - Message structure
        """
        messages = conversation.get('messages', [])
        scammer_messages = [m for m in messages if m.get('role') == 'scammer']
        
        # Combine all scammer text
        all_text = ' '.join([m.get('content', '') for m in scammer_messages])
        
        # Feature vector
        features = []
        
        # 1. Scam type (one-hot encoding)
        scam_types = ['loan_approval', 'prize_lottery', 'investment', 'digital_arrest', 'other']
        scam_type = conversation.get('scam_type', 'other')
        scam_encoding = [1.0 if st == scam_type else 0.0 for st in scam_types]
        features.extend(scam_encoding)
        
        # 2. Message count
        features.append(len(scammer_messages) / 20.0)  # Normalized
        
        # 3. Average message length
        avg_length = np.mean([len(m.get('content', '')) for m in scammer_messages]) if scammer_messages else 0
        features.append(avg_length / 200.0)  # Normalized
        
        # 4. Key phrase indicators
        key_phrases = {
            'money_mention': r'₹\s*\d+',
            'urgency': r'(immediately|urgent|now|today)',
            'authority': r'(police|government|official|bank)',
            'reward': r'(win|won|prize|approved)',
            'payment': r'(pay|payment|transfer|upi)'
        }
        
        for phrase_type, pattern in key_phrases.items():
            count = len(re.findall(pattern, all_text, re.IGNORECASE))
            features.append(min(count / 5.0, 1.0))  # Normalized, capped at 1
        
        # 5. Entity patterns
        entities = conversation.get('extracted_entities', {})
        features.append(min(len(entities.get('upi_ids', [])) / 3.0, 1.0))
        features.append(min(len(entities.get('phone_numbers', [])) / 3.0, 1.0))
        features.append(min(len(entities.get('phishing_links', [])) / 3.0, 1.0))
        
        # 6. Time of day pattern
        hour = datetime.now().hour
        time_encoding = [
            1.0 if 5 <= hour < 12 else 0.0,   # Morning
            1.0 if 12 <= hour < 17 else 0.0,  # Afternoon
            1.0 if 17 <= hour < 21 else 0.0,  # Evening
            1.0 if hour >= 21 or hour < 5 else 0.0  # Night
        ]
        features.extend(time_encoding)
        
        return np.array(features)
    
    def _cluster_conversations(self, features: np.ndarray, 
                              threshold: float,
                              min_samples: int) -> Dict[int, List[int]]:
        """Cluster conversations using DBSCAN"""
        
        # Calculate pairwise similarities
        similarities = cosine_similarity(features)
        
        # Convert similarity to distance
        distances = 1 - similarities
        
        # Cluster using DBSCAN
        clustering = DBSCAN(
            eps=1 - threshold,  # Convert similarity threshold to distance
            min_samples=min_samples,
            metric='precomputed'
        )
        
        labels = clustering.fit_predict(distances)
        
        # Group by cluster
        clusters = {}
        for idx, label in enumerate(labels):
            if label != -1:  # Ignore noise points
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(idx)
        
        return clusters
    
    def _analyze_campaign(self, conversations: List[Dict], cluster_id: int) -> Dict:
        """Analyze a campaign cluster"""
        
        campaign_id = f"camp_{cluster_id}_{datetime.now().strftime('%Y%m%d')}"
        
        # Extract campaign characteristics
        scam_types = [c.get('scam_type') for c in conversations]
        most_common_scam = Counter(scam_types).most_common(1)[0][0] if scam_types else 'unknown'
        
        # Get all messages
        all_messages = []
        for conv in conversations:
            all_messages.extend([m for m in conv.get('messages', []) if m.get('role') == 'scammer'])
        
        # Extract common script template
        script_template = self._extract_script_template(all_messages)
        
        # Get unique entities
        all_entities = {
            'upi_ids': set(),
            'phone_numbers': set(),
            'phishing_links': set(),
            'account_numbers': set()
        }
        
        for conv in conversations:
            entities = conv.get('extracted_entities', {})
            for entity_type in all_entities.keys():
                all_entities[entity_type].update(entities.get(entity_type, []))
        
        # Timeline
        timestamps = []
        for conv in conversations:
            try:
                ts = datetime.fromisoformat(conv.get('start_time', ''))
                timestamps.append(ts)
            except:
                pass
        
        start_date = min(timestamps) if timestamps else datetime.now()
        end_date = max(timestamps) if timestamps else datetime.now()
        
        # Calculate campaign metrics
        total_conversations = len(conversations)
        avg_risk_score = np.mean([c.get('risk_score', 0) for c in conversations])
        
        # Identify campaign evolution
        evolution = self._track_campaign_evolution(conversations)
        
        return {
            'campaign_id': campaign_id,
            'scam_type': most_common_scam,
            'conversation_count': total_conversations,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'duration_days': (end_date - start_date).days,
            'unique_numbers': len(all_entities['phone_numbers']),
            'unique_upi_ids': len(all_entities['upi_ids']),
            'unique_links': len(all_entities['phishing_links']),
            'script_template': script_template,
            'avg_risk_score': avg_risk_score,
            'evolution': evolution,
            'conversation_ids': [c.get('conversation_id') for c in conversations],
            'status': 'active' if (datetime.now() - end_date).days < 7 else 'inactive',
            'threat_level': 'high' if avg_risk_score > 0.7 else 'medium' if avg_risk_score > 0.4 else 'low'
        }
    
    def _extract_script_template(self, messages: List[Dict]) -> str:
        """Extract common script template from messages"""
        
        if not messages:
            return ""
        
        # Get first messages (likely to be similar)
        first_messages = [m.get('content', '') for m in messages[:min(10, len(messages))]]
        
        # Find common phrases
        all_text = ' '.join(first_messages)
        
        # Extract sentences
        sentences = re.split(r'[.!?]+', all_text)
        sentence_counts = Counter(sentences)
        
        # Get most common sentence as template
        if sentence_counts:
            template = sentence_counts.most_common(1)[0][0].strip()
            return template if len(template) > 20 else all_text[:200]
        
        return all_text[:200]
    
    def _track_campaign_evolution(self, conversations: List[Dict]) -> List[Dict]:
        """Track how campaign evolved over time"""
        
        # Sort by timestamp
        sorted_convs = sorted(
            conversations,
            key=lambda x: x.get('start_time', ''),
        )
        
        evolution = []
        
        for i, conv in enumerate(sorted_convs):
            evolution.append({
                'stage': i + 1,
                'timestamp': conv.get('start_time'),
                'risk_score': conv.get('risk_score', 0),
                'entities_extracted': sum(len(v) if isinstance(v, list) else 0 
                                        for v in conv.get('extracted_entities', {}).values()),
                'conversation_phase': conv.get('conversation_phase')
            })
        
        return evolution
    
    def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """Get campaign by ID"""
        return self.campaigns.get(campaign_id)
    
    def list_active_campaigns(self) -> List[Dict]:
        """List all active campaigns"""
        return [c for c in self.campaigns.values() if c.get('status') == 'active']
    
    def get_campaign_statistics(self) -> Dict:
        """Get overall campaign statistics"""
        if not self.campaigns:
            return {}
        
        campaigns = list(self.campaigns.values())
        
        return {
            'total_campaigns': len(campaigns),
            'active_campaigns': len([c for c in campaigns if c.get('status') == 'active']),
            'inactive_campaigns': len([c for c in campaigns if c.get('status') == 'inactive']),
            'scam_type_distribution': Counter([c.get('scam_type') for c in campaigns]),
            'avg_conversations_per_campaign': np.mean([c.get('conversation_count', 0) for c in campaigns]),
            'total_conversations_tracked': sum(c.get('conversation_count', 0) for c in campaigns),
            'threat_level_distribution': Counter([c.get('threat_level') for c in campaigns])
        }
    
    def export_campaign_report(self, campaign_id: str) -> str:
        """Export detailed campaign report"""
        campaign = self.get_campaign(campaign_id)
        
        if not campaign:
            return "Campaign not found"
        
        report = []
        report.append("=" * 70)
        report.append(f"CAMPAIGN INTELLIGENCE REPORT: {campaign_id}")
        report.append("=" * 70)
        report.append("")
        
        report.append(f"Scam Type: {campaign['scam_type'].upper()}")
        report.append(f"Status: {campaign['status'].upper()}")
        report.append(f"Threat Level: {campaign['threat_level'].upper()}")
        report.append("")
        
        report.append("TIMELINE:")
        report.append(f"  Start Date: {campaign['start_date']}")
        report.append(f"  End Date: {campaign['end_date']}")
        report.append(f"  Duration: {campaign['duration_days']} days")
        report.append("")
        
        report.append("SCALE:")
        report.append(f"  Total Conversations: {campaign['conversation_count']}")
        report.append(f"  Unique Phone Numbers: {campaign['unique_numbers']}")
        report.append(f"  Unique UPI IDs: {campaign['unique_upi_ids']}")
        report.append(f"  Unique Phishing Links: {campaign['unique_links']}")
        report.append("")
        
        report.append("SCRIPT TEMPLATE:")
        report.append(f"  {campaign['script_template']}")
        report.append("")
        
        report.append("RISK ASSESSMENT:")
        report.append(f"  Average Risk Score: {campaign['avg_risk_score']:.2f}")
        report.append("")
        
        report.append("EVOLUTION:")
        for stage in campaign['evolution'][:5]:  # First 5 stages
            report.append(f"  Stage {stage['stage']}: Risk {stage['risk_score']:.2f}, "
                        f"Entities: {stage['entities_extracted']}")
        report.append("")
        
        return "\n".join(report)


# Global instance
campaign_detector = CampaignDetector()


# Convenience functions
def detect_campaigns(conversations: List[Dict], 
                    similarity_threshold: float = 0.7) -> List[Dict]:
    """Detect fraud campaigns from conversations"""
    return campaign_detector.detect_campaigns(conversations, similarity_threshold)


def get_active_campaigns() -> List[Dict]:
    """Get all active campaigns"""
    return campaign_detector.list_active_campaigns()


def get_campaign_stats() -> Dict:
    """Get campaign statistics"""
    return campaign_detector.get_campaign_statistics()
