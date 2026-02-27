import uuid
from datetime import datetime
from typing import Dict, Optional
from models.schemas import (
    ConversationState,
    ConversationTurn,
    ConversationPhase,
    ExtractedEntities,
    ScamType,
    PersonaType
)


class ConversationManager:
    """
    Manages conversation state and history for ongoing scam interactions
    """
    
    def __init__(self):
        # In-memory storage (in production, use database)
        self.conversations: Dict[str, ConversationState] = {}
    
    def create_conversation(
        self,
        scam_type: ScamType,
        persona: PersonaType
    ) -> ConversationState:
        """Create a new conversation"""
        
        conversation_id = str(uuid.uuid4())
        
        state = ConversationState(
            conversation_id=conversation_id,
            scam_type=scam_type,
            persona=persona,
            phase=ConversationPhase.TRUST_BUILDING,
            turn_number=0,
            turns=[],
            extracted_entities=ExtractedEntities(),
            risk_score=0.0,
            context_summary="",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.conversations[conversation_id] = state
        return state
    
    def get_conversation(self, conversation_id: str) -> Optional[ConversationState]:
        """Retrieve conversation by ID"""
        return self.conversations.get(conversation_id)
    
    def add_turn(
        self,
        conversation_id: str,
        scammer_message: str,
        agent_response: str,
        entities_extracted: ExtractedEntities,
        internal_reasoning: str = ""
    ) -> ConversationState:
        """Add a new turn to the conversation"""
        
        state = self.conversations.get(conversation_id)
        if not state:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        # Increment turn number
        state.turn_number += 1
        
        # Create turn record
        turn = ConversationTurn(
            turn_number=state.turn_number,
            scammer_message=scammer_message,
            agent_response=agent_response,
            timestamp=datetime.utcnow(),
            entities_extracted=entities_extracted,
            internal_reasoning=internal_reasoning
        )
        
        state.turns.append(turn)
        
        # Merge extracted entities
        state.extracted_entities = self._merge_entities(
            state.extracted_entities,
            entities_extracted
        )
        
        # Update conversation phase based on turn number
        state.phase = self._determine_phase(state.turn_number)
        
        # Update timestamp
        state.updated_at = datetime.utcnow()
        
        # Update context summary
        state.context_summary = self._generate_context_summary(state)
        
        return state
    
    def update_risk_score(self, conversation_id: str, risk_score: float):
        """Update risk score for conversation"""
        state = self.conversations.get(conversation_id)
        if state:
            state.risk_score = risk_score
            state.updated_at = datetime.utcnow()
    
    def _merge_entities(
        self,
        existing: ExtractedEntities,
        new: ExtractedEntities
    ) -> ExtractedEntities:
        """Merge new entities with existing ones"""
        
        merged = ExtractedEntities()
        
        # Merge UPI IDs
        all_upi = set(existing.upi_ids + new.upi_ids)
        merged.upi_ids = list(all_upi)
        
        # Merge phone numbers
        all_phones = set(existing.phone_numbers + new.phone_numbers)
        merged.phone_numbers = list(all_phones)
        
        # Merge bank accounts (avoid duplicates by account number)
        all_accounts = existing.bank_accounts + new.bank_accounts
        seen_accounts = set()
        unique_accounts = []
        for acc in all_accounts:
            if acc.account_number not in seen_accounts:
                seen_accounts.add(acc.account_number)
                unique_accounts.append(acc)
        merged.bank_accounts = unique_accounts
        
        # Merge URLs
        all_urls = set(existing.phishing_links + new.phishing_links)
        merged.phishing_links = list(all_urls)
        
        # Merge aliases
        all_aliases = set(existing.aliases + new.aliases)
        merged.aliases = list(all_aliases)
        
        # Merge organizations
        all_orgs = set(existing.fake_organizations + new.fake_organizations)
        merged.fake_organizations = list(all_orgs)
        
        return merged
    
    def _determine_phase(self, turn_number: int) -> ConversationPhase:
        """Determine conversation phase based on turn number"""
        
        if turn_number <= 3:
            return ConversationPhase.TRUST_BUILDING
        elif turn_number <= 7:
            return ConversationPhase.INFORMATION_GATHERING
        elif turn_number <= 12:
            return ConversationPhase.INTELLIGENCE_EXTRACTION
        else:
            return ConversationPhase.SAFE_EXIT
    
    def _generate_context_summary(self, state: ConversationState) -> str:
        """Generate a brief context summary for AI agents"""
        
        if not state.turns:
            return ""
        
        # Get last 3 turns for context
        recent_turns = state.turns[-3:]
        
        summary_parts = []
        for turn in recent_turns:
            summary_parts.append(f"Scammer: {turn.scammer_message}")
            summary_parts.append(f"Agent: {turn.agent_response}")
        
        return "\n".join(summary_parts)
    
    def get_full_transcript(self, conversation_id: str) -> str:
        """Get full conversation transcript as text"""
        
        state = self.conversations.get(conversation_id)
        if not state:
            return ""
        
        transcript_parts = []
        for turn in state.turns:
            transcript_parts.append(f"[Turn {turn.turn_number}]")
            transcript_parts.append(f"Scammer: {turn.scammer_message}")
            transcript_parts.append(f"Agent ({state.persona.value}): {turn.agent_response}")
            transcript_parts.append("")
        
        return "\n".join(transcript_parts)
    
    def should_continue_conversation(self, conversation_id: str) -> bool:
        """Determine if conversation should continue"""
        
        state = self.conversations.get(conversation_id)
        if not state:
            return False
        
        # Stop after 15 turns (diminishing returns)
        if state.turn_number >= 15:
            return False
        
        # Stop if in safe exit phase and have extracted some intelligence
        if state.phase == ConversationPhase.SAFE_EXIT:
            has_intel = (
                len(state.extracted_entities.upi_ids) > 0 or
                len(state.extracted_entities.bank_accounts) > 0 or
                len(state.extracted_entities.phishing_links) > 0
            )
            if has_intel:
                return False
        
        return True
    
    def get_conversation_stats(self, conversation_id: str) -> Dict:
        """Get statistics about the conversation"""
        
        state = self.conversations.get(conversation_id)
        if not state:
            return {}
        
        return {
            "conversation_id": conversation_id,
            "total_turns": state.turn_number,
            "current_phase": state.phase.value,
            "scam_type": state.scam_type.value if state.scam_type else "unknown",
            "persona_used": state.persona.value if state.persona else "unknown",
            "entities_extracted": {
                "upi_ids": len(state.extracted_entities.upi_ids),
                "bank_accounts": len(state.extracted_entities.bank_accounts),
                "phishing_links": len(state.extracted_entities.phishing_links),
                "phone_numbers": len(state.extracted_entities.phone_numbers),
                "aliases": len(state.extracted_entities.aliases),
                "fake_organizations": len(state.extracted_entities.fake_organizations),
            },
            "risk_score": state.risk_score,
            "duration_seconds": (state.updated_at - state.created_at).total_seconds(),
            "created_at": state.created_at.isoformat(),
            "updated_at": state.updated_at.isoformat()
        }
    
    def list_all_conversations(self) -> list:
        """List all conversation IDs and basic info"""
        return [
            {
                "conversation_id": conv_id,
                "scam_type": state.scam_type.value if state.scam_type else "unknown",
                "turns": state.turn_number,
                "phase": state.phase.value,
                "created_at": state.created_at.isoformat()
            }
            for conv_id, state in self.conversations.items()
        ]
