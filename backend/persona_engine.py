"""
Persona Engine
Loads the 1000+ response dataset and provides context-aware replies.
"""
import json
import random
import os

class PersonaEngine:
    def __init__(self):
        # backend/persona_engine.py -> backend/data/response_dataset.json
        self.dataset_path = os.path.join(os.path.dirname(__file__), "data", "response_dataset.json")
        self.dataset = self._load_dataset()
        self.active_persona = "cautious" # Default
        
    def _load_dataset(self):
        try:
            with open(self.dataset_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return {}

    def set_persona(self, persona_type):
        if persona_type in self.dataset:
            self.active_persona = persona_type
            
    def get_response_options(self, phase="trust_building"):
        """
        Get a list of possible responses for the current persona and phase.
        Phase options: 'trust_building', 'information_gathering', 'extraction'
        """
        persona_data = self.dataset.get(self.active_persona, {})
        return persona_data.get(phase, [])
        
    def get_random_response(self, phase="trust_building"):
        options = self.get_response_options(phase)
        if options:
            return random.choice(options)
        return None

persona_engine = PersonaEngine()
