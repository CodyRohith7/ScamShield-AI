"""
Language Mirroring Engine - Adapt to scammer's communication style
"""

import re
from typing import Dict, List
from collections import Counter
import random


class LanguageMirroringEngine:
    """Learn and mirror scammer's language patterns"""
    
    def __init__(self):
        self.slang_dict = Counter()
        self.emoji_patterns = Counter()
        self.hinglish_patterns = Counter()
        self.phrase_patterns = Counter()
        self.conversation_style = {}
    
    def learn_from_conversation(self, scammer_messages: List[Dict]):
        """Learn language patterns from scammer messages"""
        
        for msg in scammer_messages:
            content = msg.get('content', '')
            
            # Extract and learn slang
            slang = self._extract_slang(content)
            self.slang_dict.update(slang)
            
            # Extract emojis
            emojis = self._extract_emojis(content)
            self.emoji_patterns.update(emojis)
            
            # Extract Hinglish words
            hinglish = self._extract_hinglish(content)
            self.hinglish_patterns.update(hinglish)
            
            # Extract common phrases
            phrases = self._extract_phrases(content)
            self.phrase_patterns.update(phrases)
        
        # Analyze overall style
        self._analyze_style(scammer_messages)
    
    def mirror_language(self, base_response: str, intensity: float = 0.5) -> str:
        """
        Mirror scammer's language in the response
        
        Args:
            base_response: Original response text
            intensity: How much to mirror (0-1)
        
        Returns:
            Modified response with mirrored language
        """
        response = base_response
        
        # Add slang (based on intensity)
        if random.random() < intensity:
            response = self._inject_slang(response, int(3 * intensity))
        
        # Add emojis
        if random.random() < intensity:
            response = self._add_emojis(response, int(2 * intensity))
        
        # Convert to Hinglish if scammer uses it
        if self._is_hinglish_conversation() and random.random() < intensity:
            response = self._add_hinglish(response)
        
        # Mirror punctuation style
        if random.random() < intensity * 0.7:
            response = self._mirror_punctuation(response)
        
        # Mirror capitalization
        if random.random() < intensity * 0.5:
            response = self._mirror_capitalization(response)
        
        return response
    
    def _extract_slang(self, text: str) -> List[str]:
        """Extract slang words"""
        slang_words = [
            'bro', 'dude', 'yaar', 'bhai', 'boss', 'sir', 'madam', 'ji',
            'anna', 'akka', 'bhaiya', 'didi', 'uncle', 'aunty'
        ]
        
        found = []
        text_lower = text.lower()
        
        for slang in slang_words:
            if slang in text_lower:
                found.append(slang)
        
        return found
    
    def _extract_emojis(self, text: str) -> List[str]:
        """Extract emojis"""
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
        
        return emoji_pattern.findall(text)
    
    def _extract_hinglish(self, text: str) -> List[str]:
        """Extract Hinglish words"""
        hinglish_words = [
            'haan', 'nahi', 'kya', 'hai', 'acha', 'theek', 'bas', 'abhi',
            'karo', 'karna', 'hoga', 'chalega', 'samjha', 'batao', 'dekho',
            'suno', 'arre', 'oye', 'yaar', 'bhai', 'matlab', 'pakka'
        ]
        
        found = []
        text_lower = text.lower()
        
        for word in hinglish_words:
            if word in text_lower:
                found.append(word)
        
        return found
    
    def _extract_phrases(self, text: str) -> List[str]:
        """Extract common phrases (2-3 words)"""
        # Simple bigram and trigram extraction
        words = text.lower().split()
        phrases = []
        
        # Bigrams
        for i in range(len(words) - 1):
            phrases.append(f"{words[i]} {words[i+1]}")
        
        # Trigrams
        for i in range(len(words) - 2):
            phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
        
        return phrases
    
    def _analyze_style(self, messages: List[Dict]):
        """Analyze overall communication style"""
        all_text = ' '.join([m.get('content', '') for m in messages])
        
        self.conversation_style = {
            'uses_emojis': len(self.emoji_patterns) > 0,
            'uses_slang': len(self.slang_dict) > 0,
            'uses_hinglish': len(self.hinglish_patterns) > 2,
            'avg_message_length': len(all_text) / max(len(messages), 1),
            'uses_exclamation': all_text.count('!') > 2,
            'uses_question': all_text.count('?') > 2,
            'uses_caps': any(word.isupper() and len(word) > 2 for word in all_text.split())
        }
    
    def _inject_slang(self, text: str, count: int = 3) -> str:
        """Inject learned slang into text"""
        if not self.slang_dict:
            return text
        
        # Get top slang words
        top_slang = [word for word, _ in self.slang_dict.most_common(count)]
        
        if not top_slang:
            return text
        
        # Add slang at beginning or end
        if random.random() < 0.5:
            # Beginning
            slang = random.choice(top_slang)
            text = f"{slang.capitalize()}, {text}"
        else:
            # End
            slang = random.choice(top_slang)
            text = f"{text} {slang}"
        
        return text
    
    def _add_emojis(self, text: str, count: int = 2) -> str:
        """Add learned emojis to text"""
        if not self.emoji_patterns:
            # Use default emojis if none learned
            default_emojis = ['😊', '👍', '🙏', '😅', '🤔']
            emojis_to_add = random.sample(default_emojis, min(count, len(default_emojis)))
        else:
            # Use learned emojis
            top_emojis = [emoji for emoji, _ in self.emoji_patterns.most_common(count)]
            emojis_to_add = top_emojis
        
        # Add emojis at end
        text = text + ' ' + ' '.join(emojis_to_add)
        
        return text
    
    def _add_hinglish(self, text: str) -> str:
        """Convert some English words to Hinglish"""
        if not self.hinglish_patterns:
            return text
        
        # Common English to Hinglish mappings
        replacements = {
            'yes': 'haan',
            'no': 'nahi',
            'okay': 'theek hai',
            'ok': 'acha',
            'what': 'kya',
            'how': 'kaise',
            'when': 'kab',
            'where': 'kahan',
            'why': 'kyun',
            'understand': 'samjha',
            'tell': 'batao',
            'see': 'dekho',
            'listen': 'suno',
            'do': 'karo',
            'will be': 'hoga',
            'is': 'hai'
        }
        
        # Replace 1-2 words
        words_to_replace = random.sample(list(replacements.keys()), 
                                        min(2, len(replacements)))
        
        for eng, hindi in replacements.items():
            if eng in words_to_replace:
                text = re.sub(r'\b' + eng + r'\b', hindi, text, flags=re.IGNORECASE)
        
        return text
    
    def _mirror_punctuation(self, text: str) -> str:
        """Mirror punctuation style"""
        style = self.conversation_style
        
        # Add exclamation marks if scammer uses them
        if style.get('uses_exclamation', False):
            text = text.replace('.', '!', 1)  # Replace first period
        
        # Add ellipsis for hesitation
        if random.random() < 0.3:
            text = text.replace('.', '...', 1)
        
        return text
    
    def _mirror_capitalization(self, text: str) -> str:
        """Mirror capitalization patterns"""
        style = self.conversation_style
        
        # Use ALL CAPS for emphasis if scammer does
        if style.get('uses_caps', False) and random.random() < 0.3:
            words = text.split()
            if len(words) > 3:
                # Capitalize one word for emphasis
                emphasis_word = random.choice(words[1:-1])  # Not first or last
                text = text.replace(emphasis_word, emphasis_word.upper(), 1)
        
        return text
    
    def _is_hinglish_conversation(self) -> bool:
        """Check if conversation is primarily Hinglish"""
        return self.conversation_style.get('uses_hinglish', False)
    
    def get_top_slang(self, n: int = 5) -> List[str]:
        """Get top N slang words"""
        return [word for word, _ in self.slang_dict.most_common(n)]
    
    def get_top_emojis(self, n: int = 5) -> List[str]:
        """Get top N emojis"""
        return [emoji for emoji, _ in self.emoji_patterns.most_common(n)]
    
    def get_style_summary(self) -> Dict:
        """Get summary of learned style"""
        return {
            'conversation_style': self.conversation_style,
            'top_slang': self.get_top_slang(5),
            'top_emojis': self.get_top_emojis(5),
            'hinglish_words_count': len(self.hinglish_patterns),
            'unique_phrases': len(self.phrase_patterns)
        }
    
    def reset(self):
        """Reset learned patterns"""
        self.slang_dict.clear()
        self.emoji_patterns.clear()
        self.hinglish_patterns.clear()
        self.phrase_patterns.clear()
        self.conversation_style.clear()


# Global instance
language_mirror = LanguageMirroringEngine()


# Convenience functions
def learn_from_messages(scammer_messages: List[Dict]):
    """Learn language patterns from scammer"""
    language_mirror.learn_from_conversation(scammer_messages)


def mirror_response(base_response: str, intensity: float = 0.5) -> str:
    """Mirror scammer's language in response"""
    return language_mirror.mirror_language(base_response, intensity)


def get_style_summary() -> Dict:
    """Get learned style summary"""
    return language_mirror.get_style_summary()
