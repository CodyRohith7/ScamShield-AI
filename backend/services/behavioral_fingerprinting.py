"""
Behavioral Fingerprinting - Identify scammers across conversations
"""

import re
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from collections import Counter
import json


class BehavioralFingerprinter:
    """Create and match behavioral fingerprints of scammers"""
    
    def __init__(self):
        self.known_fingerprints = {}  # scammer_id -> fingerprint
        self.fingerprint_cache = {}
    
    def extract_fingerprint(self, conversation: Dict) -> Dict:
        """
        Extract behavioral fingerprint from conversation
        
        Returns dict with features:
        - avg_response_time: Average time between messages
        - avg_message_length: Average character count
        - vocabulary_richness: Unique words / total words
        - emoji_frequency: Emojis per message
        - aggression_score: Level of aggressive language
        - urgency_score: Level of urgency indicators
        - time_pattern: Preferred time of day
        - language_style: Hinglish, English, etc.
        - punctuation_pattern: Usage of !, ?, ...
        - capitalization_pattern: ALL CAPS usage
        """
        messages = conversation.get('messages', [])
        
        # Filter scammer messages only
        scammer_messages = [m for m in messages if m.get('role') == 'scammer']
        
        if not scammer_messages:
            return {}
        
        # Extract all features
        fingerprint = {
            'avg_response_time': self._calc_avg_response_time(messages),
            'avg_message_length': self._calc_avg_message_length(scammer_messages),
            'vocabulary_richness': self._calc_vocabulary_richness(scammer_messages),
            'emoji_frequency': self._calc_emoji_frequency(scammer_messages),
            'aggression_score': self._calc_aggression_score(scammer_messages),
            'urgency_score': self._calc_urgency_score(scammer_messages),
            'time_pattern': self._get_time_pattern(scammer_messages),
            'language_style': self._detect_language_style(scammer_messages),
            'punctuation_pattern': self._analyze_punctuation(scammer_messages),
            'capitalization_pattern': self._analyze_capitalization(scammer_messages),
            'message_count': len(scammer_messages),
            'conversation_id': conversation.get('conversation_id'),
            'created_at': datetime.now().isoformat()
        }
        
        return fingerprint
    
    def _calc_avg_response_time(self, messages: List[Dict]) -> float:
        """Calculate average response time in seconds"""
        if len(messages) < 2:
            return 0.0
        
        response_times = []
        for i in range(1, len(messages)):
            try:
                prev_time = datetime.fromisoformat(messages[i-1].get('timestamp', ''))
                curr_time = datetime.fromisoformat(messages[i].get('timestamp', ''))
                diff = (curr_time - prev_time).total_seconds()
                if 0 < diff < 300:  # Ignore outliers (> 5 mins)
                    response_times.append(diff)
            except:
                pass
        
        return np.mean(response_times) if response_times else 45.0
    
    def _calc_avg_message_length(self, messages: List[Dict]) -> float:
        """Calculate average message length"""
        lengths = [len(m.get('content', '')) for m in messages]
        return np.mean(lengths) if lengths else 0.0
    
    def _calc_vocabulary_richness(self, messages: List[Dict]) -> float:
        """Calculate vocabulary richness (unique words / total words)"""
        all_text = ' '.join([m.get('content', '') for m in messages])
        words = re.findall(r'\b\w+\b', all_text.lower())
        
        if not words:
            return 0.0
        
        unique_words = len(set(words))
        total_words = len(words)
        
        return unique_words / total_words if total_words > 0 else 0.0
    
    def _calc_emoji_frequency(self, messages: List[Dict]) -> float:
        """Calculate emoji usage frequency"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        
        total_emojis = 0
        for msg in messages:
            content = msg.get('content', '')
            emojis = emoji_pattern.findall(content)
            total_emojis += len(emojis)
        
        return total_emojis / len(messages) if messages else 0.0
    
    def _calc_aggression_score(self, messages: List[Dict]) -> float:
        """Calculate aggression level (0-1)"""
        aggressive_words = [
            'must', 'immediately', 'now', 'urgent', 'warning', 'arrest', 'police',
            'jail', 'court', 'legal action', 'fine', 'penalty', 'seize', 'freeze',
            'block', 'suspend', 'terminate', 'cancel'
        ]
        
        all_text = ' '.join([m.get('content', '') for m in messages]).lower()
        
        count = sum(1 for word in aggressive_words if word in all_text)
        
        # Normalize by message count
        score = min(count / max(len(messages), 1), 1.0)
        
        return score
    
    def _calc_urgency_score(self, messages: List[Dict]) -> float:
        """Calculate urgency level (0-1)"""
        urgency_indicators = [
            'today', 'now', 'immediately', 'urgent', 'hurry', 'quick', 'fast',
            'limited time', 'expires', 'deadline', 'last chance', 'only',
            'within', 'hours', 'minutes'
        ]
        
        all_text = ' '.join([m.get('content', '') for m in messages]).lower()
        
        count = sum(1 for indicator in urgency_indicators if indicator in all_text)
        
        # Normalize
        score = min(count / max(len(messages), 1), 1.0)
        
        return score
    
    def _get_time_pattern(self, messages: List[Dict]) -> str:
        """Determine preferred time of day for messaging"""
        hours = []
        
        for msg in messages:
            try:
                timestamp = datetime.fromisoformat(msg.get('timestamp', ''))
                hours.append(timestamp.hour)
            except:
                pass
        
        if not hours:
            return 'unknown'
        
        avg_hour = np.mean(hours)
        
        if 5 <= avg_hour < 12:
            return 'morning'
        elif 12 <= avg_hour < 17:
            return 'afternoon'
        elif 17 <= avg_hour < 21:
            return 'evening'
        else:
            return 'night'
    
    def _detect_language_style(self, messages: List[Dict]) -> str:
        """Detect language style (English, Hinglish, etc.)"""
        all_text = ' '.join([m.get('content', '') for m in messages]).lower()
        
        # Hinglish indicators
        hinglish_words = ['bhai', 'yaar', 'kya', 'hai', 'haan', 'nahi', 'acha', 'theek']
        hinglish_count = sum(1 for word in hinglish_words if word in all_text)
        
        # Tamil indicators
        tamil_words = ['anna', 'enakku', 'neenga', 'irukku', 'ponga']
        tamil_count = sum(1 for word in tamil_words if word in all_text)
        
        if hinglish_count > 2:
            return 'hinglish'
        elif tamil_count > 2:
            return 'tamil'
        else:
            return 'english'
    
    def _analyze_punctuation(self, messages: List[Dict]) -> Dict:
        """Analyze punctuation usage patterns"""
        all_text = ' '.join([m.get('content', '') for m in messages])
        
        return {
            'exclamation_marks': all_text.count('!') / max(len(messages), 1),
            'question_marks': all_text.count('?') / max(len(messages), 1),
            'ellipsis': all_text.count('...') / max(len(messages), 1),
            'periods': all_text.count('.') / max(len(messages), 1)
        }
    
    def _analyze_capitalization(self, messages: List[Dict]) -> float:
        """Analyze ALL CAPS usage"""
        all_caps_count = 0
        
        for msg in messages:
            content = msg.get('content', '')
            words = content.split()
            
            for word in words:
                if len(word) > 2 and word.isupper():
                    all_caps_count += 1
        
        total_words = sum(len(m.get('content', '').split()) for m in messages)
        
        return all_caps_count / max(total_words, 1)
    
    def match_fingerprint(self, new_fingerprint: Dict, threshold: float = 0.85) -> Dict:
        """
        Match fingerprint against known scammers
        
        Returns:
            {
                'match': bool,
                'scammer_id': str or None,
                'similarity': float,
                'confidence': str (low/medium/high)
            }
        """
        if not self.known_fingerprints:
            return {'match': False, 'scammer_id': None, 'similarity': 0.0, 'confidence': 'none'}
        
        best_match = None
        best_similarity = 0.0
        
        for scammer_id, known_fp in self.known_fingerprints.items():
            similarity = self._calculate_similarity(new_fingerprint, known_fp)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = scammer_id
        
        # Determine confidence level
        if best_similarity >= 0.9:
            confidence = 'high'
        elif best_similarity >= 0.8:
            confidence = 'medium'
        elif best_similarity >= 0.7:
            confidence = 'low'
        else:
            confidence = 'very_low'
        
        return {
            'match': best_similarity >= threshold,
            'scammer_id': best_match if best_similarity >= threshold else None,
            'similarity': best_similarity,
            'confidence': confidence,
            'all_matches': self._get_all_matches(new_fingerprint, threshold=0.7)
        }
    
    def _calculate_similarity(self, fp1: Dict, fp2: Dict) -> float:
        """Calculate similarity between two fingerprints (0-1)"""
        
        # Weighted features
        weights = {
            'avg_response_time': 0.15,
            'avg_message_length': 0.10,
            'vocabulary_richness': 0.15,
            'emoji_frequency': 0.10,
            'aggression_score': 0.15,
            'urgency_score': 0.15,
            'time_pattern': 0.10,
            'language_style': 0.10
        }
        
        total_similarity = 0.0
        
        for feature, weight in weights.items():
            if feature in fp1 and feature in fp2:
                if isinstance(fp1[feature], (int, float)):
                    # Numerical features - use normalized difference
                    val1 = fp1[feature]
                    val2 = fp2[feature]
                    max_val = max(val1, val2, 1.0)
                    diff = abs(val1 - val2) / max_val
                    similarity = 1.0 - diff
                else:
                    # Categorical features - exact match
                    similarity = 1.0 if fp1[feature] == fp2[feature] else 0.0
                
                total_similarity += similarity * weight
        
        return total_similarity
    
    def _get_all_matches(self, fingerprint: Dict, threshold: float = 0.7) -> List[Dict]:
        """Get all matches above threshold"""
        matches = []
        
        for scammer_id, known_fp in self.known_fingerprints.items():
            similarity = self._calculate_similarity(fingerprint, known_fp)
            
            if similarity >= threshold:
                matches.append({
                    'scammer_id': scammer_id,
                    'similarity': similarity,
                    'confidence': 'high' if similarity >= 0.9 else 'medium' if similarity >= 0.8 else 'low'
                })
        
        # Sort by similarity
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        
        return matches
    
    def register_fingerprint(self, scammer_id: str, fingerprint: Dict):
        """Register a new scammer fingerprint"""
        self.known_fingerprints[scammer_id] = fingerprint
    
    def save_fingerprints(self, filepath: str = "data/fingerprints.json"):
        """Save fingerprints to file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.known_fingerprints, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving fingerprints: {e}")
            return False
    
    def load_fingerprints(self, filepath: str = "data/fingerprints.json"):
        """Load fingerprints from file"""
        try:
            with open(filepath, 'r') as f:
                self.known_fingerprints = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading fingerprints: {e}")
            return False


# Global instance
fingerprinter = BehavioralFingerprinter()


# Convenience functions
def extract_fingerprint(conversation: Dict) -> Dict:
    """Extract behavioral fingerprint from conversation"""
    return fingerprinter.extract_fingerprint(conversation)


def match_fingerprint(fingerprint: Dict, threshold: float = 0.85) -> Dict:
    """Match fingerprint against known scammers"""
    return fingerprinter.match_fingerprint(fingerprint, threshold)


def register_scammer(scammer_id: str, fingerprint: Dict):
    """Register new scammer fingerprint"""
    fingerprinter.register_fingerprint(scammer_id, fingerprint)
