"""
Tactic Taxonomy - Real-time detection and classification of scammer tactics
"""

import re
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TacticDetection:
    """Detected tactic with metadata"""
    tactic: str
    confidence: float
    keywords_matched: List[str]
    context: str
    timestamp: str


class TacticTaxonomyEngine:
    """Detect and classify scammer tactics in real-time"""
    
    # Tactic definitions with keywords and patterns
    TACTICS = {
        'fear': {
            'keywords': [
                'arrest', 'police', 'jail', 'prison', 'legal action', 'court',
                'fine', 'penalty', 'seize', 'freeze', 'block', 'suspend',
                'terminate', 'cancel', 'criminal', 'fraud', 'investigation',
                'warrant', 'summons', 'lawsuit', 'prosecution', 'charges'
            ],
            'patterns': [
                r'you will be arrested',
                r'legal action will be taken',
                r'police will come',
                r'account will be frozen',
                r'criminal case'
            ],
            'weight': 1.0
        },
        'urgency': {
            'keywords': [
                'immediately', 'now', 'urgent', 'hurry', 'quick', 'fast',
                'today', 'within', 'deadline', 'expires', 'limited time',
                'last chance', 'only', 'minutes', 'hours', 'soon',
                'asap', 'right now', 'instant', 'emergency'
            ],
            'patterns': [
                r'today only',
                r'limited time',
                r'expires in \d+',
                r'within \d+ (hours|minutes)',
                r'last chance',
                r'act now'
            ],
            'weight': 0.9
        },
        'authority': {
            'keywords': [
                'government', 'official', 'officer', 'department', 'ministry',
                'rbi', 'sebi', 'income tax', 'cbi', 'police', 'bank',
                'authorized', 'certified', 'registered', 'licensed',
                'inspector', 'commissioner', 'director'
            ],
            'patterns': [
                r'i am (officer|inspector|from)',
                r'government (official|department)',
                r'authorized by',
                r'official (notice|communication)'
            ],
            'weight': 1.0
        },
        'reward': {
            'keywords': [
                'win', 'won', 'prize', 'reward', 'bonus', 'cashback',
                'refund', 'lottery', 'lucky', 'selected', 'congratulations',
                'winner', 'jackpot', 'gift', 'free', 'earn', 'profit',
                'returns', 'guaranteed', 'approved'
            ],
            'patterns': [
                r'you have won',
                r'congratulations',
                r'₹\s*\d+\s*(lakh|crore|thousand)',
                r'guaranteed returns',
                r'approved for ₹'
            ],
            'weight': 0.8
        },
        'scarcity': {
            'keywords': [
                'limited', 'exclusive', 'only', 'few', 'rare', 'special',
                'selected', 'chosen', 'unique', 'one time', 'last',
                'final', 'closing', 'ending', 'slots', 'available'
            ],
            'patterns': [
                r'only \d+ (slots|spots|places)',
                r'limited (offer|time|slots)',
                r'exclusive (offer|deal)',
                r'one time (offer|opportunity)'
            ],
            'weight': 0.7
        },
        'social_proof': {
            'keywords': [
                'people', 'customers', 'users', 'members', 'thousands',
                'lakhs', 'everyone', 'popular', 'trusted', 'verified',
                'reviewed', 'rated', 'testimonial', 'success', 'satisfied'
            ],
            'patterns': [
                r'\d+\s*(lakh|thousand|crore)\s*(people|customers)',
                r'thousands of (people|users)',
                r'everyone is (doing|using)',
                r'trusted by \d+'
            ],
            'weight': 0.6
        },
        'reciprocity': {
            'keywords': [
                'help', 'assist', 'support', 'service', 'favor', 'benefit',
                'advantage', 'opportunity', 'chance', 'offer', 'provide',
                'give', 'grant', 'allow'
            ],
            'patterns': [
                r'we (will|can) help you',
                r'let me (help|assist)',
                r'i can (provide|give|offer)'
            ],
            'weight': 0.5
        },
        'confusion': {
            'keywords': [
                'technical', 'system', 'error', 'issue', 'problem', 'glitch',
                'update', 'verification', 'confirm', 'validate', 'check',
                'review', 'process', 'procedure', 'steps'
            ],
            'patterns': [
                r'technical (issue|error|problem)',
                r'system (update|error)',
                r'verification (required|needed)',
                r'confirm your (details|information)'
            ],
            'weight': 0.6
        },
        'greed': {
            'keywords': [
                'money', 'cash', 'profit', 'earn', 'income', 'returns',
                'investment', 'double', 'triple', 'multiply', 'grow',
                'rich', 'wealthy', 'millionaire', 'passive income'
            ],
            'patterns': [
                r'earn ₹\s*\d+',
                r'(double|triple) your (money|investment)',
                r'\d+% returns',
                r'passive income'
            ],
            'weight': 0.8
        },
        'trust_building': {
            'keywords': [
                'trust', 'genuine', 'real', 'authentic', 'legitimate',
                'safe', 'secure', 'protected', 'guaranteed', 'assured',
                'certified', 'verified', 'official', 'registered'
            ],
            'patterns': [
                r'you can trust',
                r'100% (safe|genuine|secure)',
                r'guaranteed (safe|secure)',
                r'officially (registered|certified)'
            ],
            'weight': 0.5
        }
    }
    
    def __init__(self):
        self.detection_history = []
    
    def analyze_message(self, message: str) -> List[TacticDetection]:
        """
        Analyze message and detect tactics
        
        Returns list of detected tactics with confidence scores
        """
        detections = []
        message_lower = message.lower()
        
        for tactic_name, tactic_data in self.TACTICS.items():
            # Check keywords
            keywords_found = []
            for keyword in tactic_data['keywords']:
                if keyword in message_lower:
                    keywords_found.append(keyword)
            
            # Check patterns
            patterns_matched = 0
            for pattern in tactic_data['patterns']:
                if re.search(pattern, message_lower):
                    patterns_matched += 1
            
            # Calculate confidence
            if keywords_found or patterns_matched > 0:
                keyword_score = len(keywords_found) / len(tactic_data['keywords'])
                pattern_score = patterns_matched / max(len(tactic_data['patterns']), 1)
                
                # Weighted combination
                confidence = (keyword_score * 0.6 + pattern_score * 0.4) * tactic_data['weight']
                
                # Only include if confidence > threshold
                if confidence > 0.1:
                    detection = TacticDetection(
                        tactic=tactic_name,
                        confidence=min(confidence, 1.0),
                        keywords_matched=keywords_found[:5],  # Top 5
                        context=message[:100],  # First 100 chars
                        timestamp=datetime.now().isoformat()
                    )
                    detections.append(detection)
        
        # Sort by confidence
        detections.sort(key=lambda x: x.confidence, reverse=True)
        
        # Store in history
        self.detection_history.extend(detections)
        
        return detections
    
    def analyze_conversation(self, messages: List[Dict]) -> Dict:
        """
        Analyze entire conversation for tactic patterns
        
        Returns:
            {
                'tactic_sequence': List of tactics in order,
                'dominant_tactics': Top 3 tactics,
                'tactic_distribution': Count of each tactic,
                'threat_level': Overall threat assessment,
                'timeline': Tactic usage over time
            }
        """
        all_detections = []
        tactic_counts = {tactic: 0 for tactic in self.TACTICS.keys()}
        tactic_timeline = []
        
        # Analyze each message
        for msg in messages:
            if msg.get('role') == 'scammer':
                content = msg.get('content', '')
                detections = self.analyze_message(content)
                
                for detection in detections:
                    all_detections.append(detection)
                    tactic_counts[detection.tactic] += 1
                    
                    tactic_timeline.append({
                        'timestamp': msg.get('timestamp', ''),
                        'tactic': detection.tactic,
                        'confidence': detection.confidence
                    })
        
        # Get dominant tactics (top 3)
        sorted_tactics = sorted(tactic_counts.items(), key=lambda x: x[1], reverse=True)
        dominant_tactics = [
            {'tactic': tactic, 'count': count, 'percentage': count / max(sum(tactic_counts.values()), 1) * 100}
            for tactic, count in sorted_tactics[:3]
            if count > 0
        ]
        
        # Calculate threat level
        threat_level = self._calculate_threat_level(tactic_counts, all_detections)
        
        # Create tactic sequence
        tactic_sequence = [d.tactic for d in all_detections]
        
        return {
            'tactic_sequence': tactic_sequence,
            'dominant_tactics': dominant_tactics,
            'tactic_distribution': tactic_counts,
            'threat_level': threat_level,
            'timeline': tactic_timeline,
            'total_tactics_detected': len(all_detections),
            'unique_tactics': len([t for t in tactic_counts.values() if t > 0])
        }
    
    def _calculate_threat_level(self, tactic_counts: Dict, detections: List[TacticDetection]) -> str:
        """Calculate overall threat level"""
        
        # High-risk tactics
        high_risk = ['fear', 'authority', 'urgency']
        high_risk_count = sum(tactic_counts.get(t, 0) for t in high_risk)
        
        # Average confidence
        avg_confidence = sum(d.confidence for d in detections) / max(len(detections), 1)
        
        # Total tactics
        total_tactics = sum(tactic_counts.values())
        
        # Calculate score
        score = (high_risk_count * 0.5 + total_tactics * 0.3 + avg_confidence * 0.2)
        
        if score > 5:
            return 'critical'
        elif score > 3:
            return 'high'
        elif score > 1.5:
            return 'medium'
        else:
            return 'low'
    
    def get_tactic_description(self, tactic: str) -> str:
        """Get human-readable description of tactic"""
        descriptions = {
            'fear': 'Using threats and intimidation to create panic',
            'urgency': 'Creating artificial time pressure to force quick decisions',
            'authority': 'Impersonating officials or organizations to gain trust',
            'reward': 'Promising prizes, money, or benefits to lure victims',
            'scarcity': 'Claiming limited availability to create FOMO',
            'social_proof': 'Using fake testimonials or popularity claims',
            'reciprocity': 'Offering help to create obligation',
            'confusion': 'Using technical jargon to confuse victims',
            'greed': 'Appealing to desire for easy money',
            'trust_building': 'Attempting to establish credibility'
        }
        return descriptions.get(tactic, 'Unknown tactic')
    
    def get_counter_strategy(self, tactic: str) -> str:
        """Get recommended counter-strategy for tactic"""
        strategies = {
            'fear': 'Stay calm, verify claims independently, real authorities don\'t threaten over phone',
            'urgency': 'Take your time, legitimate offers don\'t expire in minutes',
            'authority': 'Ask for credentials, verify through official channels',
            'reward': 'If it sounds too good to be true, it probably is',
            'scarcity': 'Don\'t let FOMO cloud judgment, research before acting',
            'social_proof': 'Verify testimonials independently, check reviews',
            'reciprocity': 'Don\'t feel obligated, unsolicited help often has strings',
            'confusion': 'Ask for simple explanations, don\'t proceed if unclear',
            'greed': 'No legitimate investment offers guaranteed high returns',
            'trust_building': 'Trust must be earned, verify all claims'
        }
        return strategies.get(tactic, 'Stay vigilant and verify all information')
    
    def export_analysis(self, conversation_analysis: Dict) -> str:
        """Export analysis as formatted report"""
        report = []
        report.append("=" * 60)
        report.append("TACTIC TAXONOMY ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        
        report.append(f"Threat Level: {conversation_analysis['threat_level'].upper()}")
        report.append(f"Total Tactics Detected: {conversation_analysis['total_tactics_detected']}")
        report.append(f"Unique Tactics Used: {conversation_analysis['unique_tactics']}")
        report.append("")
        
        report.append("DOMINANT TACTICS:")
        report.append("-" * 60)
        for tactic_info in conversation_analysis['dominant_tactics']:
            tactic = tactic_info['tactic']
            count = tactic_info['count']
            pct = tactic_info['percentage']
            report.append(f"{tactic.upper()}: {count} occurrences ({pct:.1f}%)")
            report.append(f"  Description: {self.get_tactic_description(tactic)}")
            report.append(f"  Counter: {self.get_counter_strategy(tactic)}")
            report.append("")
        
        report.append("TACTIC SEQUENCE:")
        report.append("-" * 60)
        sequence = conversation_analysis['tactic_sequence']
        report.append(" -> ".join(sequence[:10]))  # First 10
        report.append("")
        
        return "\n".join(report)


# Global instance
tactic_engine = TacticTaxonomyEngine()


# Convenience functions
def analyze_message(message: str) -> List[Dict]:
    """Analyze single message for tactics"""
    detections = tactic_engine.analyze_message(message)
    return [
        {
            'tactic': d.tactic,
            'confidence': d.confidence,
            'keywords': d.keywords_matched
        }
        for d in detections
    ]


def analyze_conversation(messages: List[Dict]) -> Dict:
    """Analyze full conversation"""
    return tactic_engine.analyze_conversation(messages)


def get_threat_assessment(messages: List[Dict]) -> str:
    """Get quick threat assessment"""
    analysis = tactic_engine.analyze_conversation(messages)
    return analysis['threat_level']
