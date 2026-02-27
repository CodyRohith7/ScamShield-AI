"""
Response Selector - Selects humanized responses based on context
"""

import json
import random
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime


class ResponseSelector:
    """Intelligent response selection from humanized dataset"""
    
    def __init__(self, dataset_path: str = "data/humanized_responses.json"):
        self.dataset_path = dataset_path
        self.responses = self._load_responses()
        self.response_history = []  # Track used responses to avoid repetition
    
    def _load_responses(self) -> Dict:
        """Load humanized responses from JSON file"""
        try:
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading responses: {e}")
            return {}
    
    def select_response(self, 
                       phase: str,
                       persona: str = "cautious_middle_aged",
                       context: Dict = None) -> str:
        """
        Select appropriate response based on context
        
        Args:
            phase: Conversation phase (trust_building, information_gathering, extraction)
            persona: Persona type (cautious_middle_aged, eager_young_adult, etc.)
            context: Additional context (scam_type, turn_number, time_of_day, etc.)
        
        Returns:
            Selected response string
        """
        context = context or {}
        
        # Get persona responses
        persona_responses = self.responses.get('personas', {}).get(persona, {})
        
        # Get phase-specific responses
        phase_responses = persona_responses.get(phase, [])
        
        if not phase_responses:
            # Fallback to common responses
            phase_responses = self._get_common_responses(phase, context)
        
        # Filter based on context
        filtered_responses = self._filter_by_context(phase_responses, context)
        
        # Select response (avoid recent repetitions)
        response = self._select_non_repetitive(filtered_responses)
        
        # Add natural variations
        response = self._add_variations(response, context)
        
        # Track usage
        self.response_history.append(response)
        if len(self.response_history) > 50:
            self.response_history.pop(0)
        
        return response
    
    def _get_common_responses(self, phase: str, context: Dict) -> List[str]:
        """Get common responses when persona-specific not available"""
        common = self.responses.get('common_responses', {})
        
        # Map phase to common response categories
        if phase == 'trust_building':
            categories = ['urgency_pushback', 'website_questions', 'upi_questions']
        elif phase == 'information_gathering':
            categories = ['buying_time', 'alternatives', 'repeated_info']
        elif phase == 'extraction':
            categories = ['building_confidence', 'fake_cooperation']
        else:
            categories = list(common.keys())
        
        responses = []
        for category in categories:
            responses.extend(common.get(category, []))
        
        return responses
    
    def _filter_by_context(self, responses: List[str], context: Dict) -> List[str]:
        """Filter responses based on context"""
        if not context:
            return responses
        
        filtered = responses.copy()
        
        # Filter by scam type
        scam_type = context.get('scam_type')
        if scam_type:
            scam_specific = self.responses.get('scam_type_specific', {}).get(scam_type, [])
            if scam_specific and random.random() < 0.3:  # 30% chance to use scam-specific
                filtered.extend(scam_specific)
        
        # Add time-of-day specific responses
        time_of_day = context.get('time_of_day') or self._get_time_of_day()
        time_responses = self.responses.get('context_based', {}).get(time_of_day, [])
        if time_responses and random.random() < 0.2:  # 20% chance
            filtered.extend(time_responses)
        
        # Add emotional responses based on turn number
        turn_number = context.get('turn_number', 0)
        if turn_number > 10:
            # Add some frustration/impatience
            emotional = self.responses.get('emotional_states', {}).get('anger', [])
            if emotional:
                filtered.extend(emotional[:2])
        elif turn_number > 5:
            # Add some caution
            emotional = self.responses.get('emotional_states', {}).get('fear', [])
            if emotional:
                filtered.extend(emotional[:2])
        
        # Add Hinglish responses randomly
        if random.random() < 0.15:  # 15% chance
            hinglish = self.responses.get('common_responses', {}).get('hinglish', [])
            if hinglish:
                filtered.extend(hinglish[:3])
        
        return filtered if filtered else responses
    
    def _select_non_repetitive(self, responses: List[str]) -> str:
        """Select response avoiding recent repetitions"""
        if not responses:
            return "I need to think about this. Can you give me some time?"
        
        # Filter out recently used responses
        available = [r for r in responses if r not in self.response_history[-10:]]
        
        if not available:
            available = responses  # Use all if everything was recent
        
        return random.choice(available)
    
    def _add_variations(self, response: str, context: Dict) -> str:
        """Add natural variations to response"""
        
        # Add filler words occasionally
        if random.random() < 0.2:
            fillers = ["Hmm, ", "Well, ", "You know, ", "Actually, ", "So, "]
            response = random.choice(fillers) + response
        
        # Add trailing thoughts occasionally
        if random.random() < 0.15:
            trails = [" I think.", " Maybe.", " Not sure.", " Let me see."]
            response = response + random.choice(trails)
        
        # Add ellipsis for hesitation
        if random.random() < 0.1:
            response = response.replace(".", "...")
        
        return response
    
    def _get_time_of_day(self) -> str:
        """Determine time of day"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        else:
            return 'evening'
    
    def get_scam_specific_response(self, scam_type: str) -> str:
        """Get scam-type specific response"""
        scam_responses = self.responses.get('scam_type_specific', {}).get(scam_type, [])
        
        if scam_responses:
            return self._select_non_repetitive(scam_responses)
        
        return self.select_response('information_gathering')
    
    def get_emotional_response(self, emotion: str) -> str:
        """Get emotion-based response"""
        emotional_responses = self.responses.get('emotional_states', {}).get(emotion, [])
        
        if emotional_responses:
            return self._select_non_repetitive(emotional_responses)
        
        return self.select_response('trust_building')
    
    def get_regional_response(self, language: str = 'hinglish') -> str:
        """Get regional language response"""
        if language == 'hinglish':
            responses = self.responses.get('common_responses', {}).get('hinglish', [])
        elif language == 'tamil':
            responses = self.responses.get('common_responses', {}).get('regional_tamil', [])
        else:
            responses = []
        
        if responses:
            return self._select_non_repetitive(responses)
        
        return self.select_response('trust_building')
    
    def get_context_aware_response(self, 
                                   phase: str,
                                   persona: str,
                                   scam_type: str,
                                   turn_number: int,
                                   suspicion_level: float = 0.5) -> str:
        """
        Get highly context-aware response
        
        Args:
            phase: Conversation phase
            persona: Persona type
            scam_type: Type of scam
            turn_number: Current turn number
            suspicion_level: How suspicious the agent should be (0-1)
        
        Returns:
            Contextually appropriate response
        """
        context = {
            'scam_type': scam_type,
            'turn_number': turn_number,
            'time_of_day': self._get_time_of_day(),
            'suspicion_level': suspicion_level
        }
        
        # Adjust persona based on suspicion level
        if suspicion_level > 0.7:
            # Be more skeptical
            persona = 'skeptical_techie'
        elif suspicion_level < 0.3:
            # Be more trusting
            persona = 'eager_young_adult'
        
        return self.select_response(phase, persona, context)
    
    def generate_multi_turn_sequence(self, 
                                    persona: str,
                                    scam_type: str,
                                    num_turns: int = 5) -> List[str]:
        """Generate a sequence of responses for multiple turns"""
        sequence = []
        
        # Start with trust building
        for i in range(min(2, num_turns)):
            response = self.select_response(
                'trust_building',
                persona,
                {'scam_type': scam_type, 'turn_number': i}
            )
            sequence.append(response)
        
        # Move to information gathering
        for i in range(2, min(num_turns - 1, num_turns)):
            response = self.select_response(
                'information_gathering',
                persona,
                {'scam_type': scam_type, 'turn_number': i}
            )
            sequence.append(response)
        
        # End with extraction
        if num_turns > 2:
            response = self.select_response(
                'extraction',
                persona,
                {'scam_type': scam_type, 'turn_number': num_turns - 1}
            )
            sequence.append(response)
        
        return sequence


# Global instance
response_selector = ResponseSelector()


# Convenience functions
def get_response(phase: str, persona: str = "cautious_middle_aged", context: Dict = None) -> str:
    """Get humanized response"""
    return response_selector.select_response(phase, persona, context)


def get_context_aware_response(phase: str, persona: str, scam_type: str, 
                               turn_number: int, suspicion_level: float = 0.5) -> str:
    """Get context-aware response"""
    return response_selector.get_context_aware_response(
        phase, persona, scam_type, turn_number, suspicion_level
    )


def get_scam_specific_response(scam_type: str) -> str:
    """Get scam-specific response"""
    return response_selector.get_scam_specific_response(scam_type)
