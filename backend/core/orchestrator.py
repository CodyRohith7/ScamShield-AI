from typing import Optional
from datetime import datetime
import os

from models.schemas import (
    EngageRequest,
    EngageResponse,
    IntelligenceReport,
    ScamType,
    PersonaType,
    ConversationPhase,
    ExtractedEntities
)
from agents.detective_agent import DetectiveAgent
from agents.persona_agent import PersonaAgent
from agents.intelligence_agent import IntelligenceAgent
from core.conversation_manager import ConversationManager
from core.entity_extractor import EntityExtractor

# NEW ADVANCED SERVICES
from utils.enhanced_entity_extractor import EnhancedEntityExtractor
from services.response_selector import ResponseSelector
from services.behavioral_fingerprinting import BehavioralFingerprinter
from services.language_mirroring import LanguageMirroringEngine
from services.tactic_taxonomy import TacticTaxonomyEngine
from database.conversation_db import ConversationDatabase


class AgentOrchestrator:
    """
    ENHANCED Main orchestrator with advanced AI features
    """
    
    def __init__(self):
        # Initialize all agents
        self.detective_agent = DetectiveAgent()
        self.persona_agent = PersonaAgent()
        self.intelligence_agent = IntelligenceAgent()
        
        # Initialize managers
        self.conversation_manager = ConversationManager()
        self.entity_extractor = EntityExtractor()
        
        # NEW ADVANCED SERVICES
        self.enhanced_extractor = EnhancedEntityExtractor()
        self.response_selector = ResponseSelector()
        self.fingerprinter = BehavioralFingerprinter()
        self.language_mirror = LanguageMirroringEngine()
        self.tactic_engine = TacticTaxonomyEngine()
        self.conversation_db = ConversationDatabase()
    
    async def engage_with_scammer(self, request: EngageRequest) -> EngageResponse:
        """
        Main method to engage with scammer message
        
        Workflow:
        1. Detective Agent analyzes message
        2. Persona Agent generates response
        3. Entity Extractor finds fraud indicators
        4. Intelligence Agent enhances extraction
        5. Return structured response
        """
        
        scammer_message = request.message
        conversation_id = request.conversation_id
        
        # Step 1: Get or create conversation
        if conversation_id:
            # Continue existing conversation
            state = self.conversation_manager.get_conversation(conversation_id)
            if not state:
                raise ValueError(f"Conversation {conversation_id} not found")
            
            scam_type = state.scam_type
            persona = state.persona
            phase = state.phase
            turn_number = state.turn_number + 1
            context = state.context_summary
            
        else:
            # New conversation - analyze with Detective Agent
            analysis = await self.detective_agent.analyze_message(scammer_message)
            
            scam_type = analysis["scam_type"]
            persona = analysis["recommended_persona"]
            
            # Create new conversation
            state = self.conversation_manager.create_conversation(
                scam_type=scam_type,
                persona=persona
            )
            conversation_id = state.conversation_id
            phase = ConversationPhase.TRUST_BUILDING
            turn_number = 1
            context = None
            
            # Update risk score from analysis
            self.conversation_manager.update_risk_score(
                conversation_id,
                analysis["risk_score"]
            )
        
        # Step 2: ENHANCED - Use humanized response selector instead of basic persona
        try:
            # Learn scammer's language patterns
            self.language_mirror.learn_from_message(scammer_message)
            
            # Detect scammer tactics
            tactics_detected = self.tactic_engine.detect_tactics(scammer_message)
            
            # Generate humanized response using response selector
            agent_response = self.response_selector.select_response(
                phase=phase.value if hasattr(phase, 'value') else str(phase),
                persona=persona.value if hasattr(persona, 'value') else str(persona),
                scam_type=scam_type.value if hasattr(scam_type, 'value') else str(scam_type),
                turn_number=turn_number,
                scammer_message=scammer_message
            )
            
            # Mirror scammer's language style
            agent_response = self.language_mirror.mirror_response(
                agent_response,
                intensity=0.6  # 60% mirroring
            )
            
            # Generate internal reasoning
            internal_reasoning = f"Using {persona} persona. Detected tactics: {', '.join([t['tactic'] for t in tactics_detected[:3]])}. Phase: {phase}."
            
        except Exception as e:
            print(f"Enhanced response generation error: {e}")
            print("Falling back to basic persona agent...")
            # Fallback to old persona agent
            agent_response, internal_reasoning = await self.persona_agent.generate_response(
                scammer_message=scammer_message,
                persona=persona,
                scam_type=scam_type,
                phase=phase,
                turn_number=turn_number,
                conversation_context=context
            )
            tactics_detected = []
        
        # Step 3: ENHANCED - Use 11-type entity extractor
        try:
            # Extract from scammer message
            enhanced_entities_obj = self.enhanced_extractor.extract_all(scammer_message)
            enhanced_entities = enhanced_entities_obj.to_dict()
            
            # Convert to old format for compatibility
            scammer_entities = self._convert_enhanced_entities(enhanced_entities)
            
            # Extract from agent response
            agent_enhanced_obj = self.enhanced_extractor.extract_all(agent_response)
            agent_entities = self._convert_enhanced_entities(agent_enhanced_obj.to_dict())
            
        except Exception as e:
            print(f"Enhanced entity extraction error: {e}")
            print("Falling back to basic entity extractor...")
            # Fallback to old extractor
            scammer_entities = self.entity_extractor.extract_from_text(scammer_message)
            agent_entities = self.entity_extractor.extract_from_text(agent_response)
            enhanced_entities = {}
        
        # Merge entities
        turn_entities = self._merge_turn_entities(scammer_entities, agent_entities)
        
        # Step 4: Enhance with AI-based extraction (if available)
        conversation_text = f"Scammer: {scammer_message}\\nAgent: {agent_response}"
        ai_entities = await self.intelligence_agent.extract_entities_ai(conversation_text)
        
        # Merge AI-extracted entities
        final_entities = self._merge_turn_entities(turn_entities, ai_entities)
        
        # Step 5: Behavioral fingerprinting
        fingerprint = self.fingerprinter.extract_fingerprint([{
            'role': 'scammer',
            'content': scammer_message,
            'timestamp': datetime.now().isoformat()
        }])
        
        # Step 6: Add turn to conversation
        state = self.conversation_manager.add_turn(
            conversation_id=conversation_id,
            scammer_message=scammer_message,
            agent_response=agent_response,
            entities_extracted=final_entities,
            internal_reasoning=internal_reasoning
        )
        
        # Save to database
        try:
            self.conversation_db.save_conversation({
                'conversation_id': conversation_id,
                'scam_type': scam_type.value if hasattr(scam_type, 'value') else str(scam_type),
                'persona_used': persona.value if hasattr(persona, 'value') else str(persona),
                'risk_score': state.risk_score,
                'conversation_phase': phase.value if hasattr(phase, 'value') else str(phase),
                'turn_count': turn_number,
                'extracted_entities': enhanced_entities,
                'tactics_detected': [t['tactic'] for t in tactics_detected],
                'behavioral_fingerprint': fingerprint,
                'messages': [{
                    'role': 'scammer',
                    'content': scammer_message,
                    'timestamp': datetime.now().isoformat()
                }, {
                    'role': 'agent',
                    'content': agent_response,
                    'timestamp': datetime.now().isoformat()
                }]
            })
        except Exception as e:
            print(f"Warning: Could not save to database: {e}")
        
        # Step 7: Calculate confidence level
        confidence_level = self._calculate_confidence(state)
        
        # Step 8: Determine if should continue
        should_continue = self.conversation_manager.should_continue_conversation(conversation_id)
        
        # Step 9: Build response
        response = EngageResponse(
            conversation_id=conversation_id,
            agent_response=agent_response,
            scam_type=scam_type,
            persona_used=persona,
            conversation_phase=phase,
            turn_number=turn_number,
            extracted_entities=state.extracted_entities,
            risk_score=state.risk_score,
            confidence_level=confidence_level,
            internal_reasoning=internal_reasoning,
            should_continue=should_continue
        )
        
        return response
    
    async def generate_intelligence_report(self, conversation_id: str) -> IntelligenceReport:
        """
        Generate final intelligence report for a conversation
        """
        
        state = self.conversation_manager.get_conversation(conversation_id)
        if not state:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        # Get full transcript
        transcript = self.conversation_manager.get_full_transcript(conversation_id)
        
        # Generate summary using Intelligence Agent
        summary = await self.intelligence_agent.generate_summary(transcript)
        
        # Identify red flags
        red_flags = await self.intelligence_agent.identify_red_flags(transcript)
        
        # Recommend actions
        recommended_actions = await self.intelligence_agent.recommend_actions(
            state.extracted_entities,
            transcript
        )
        
        # Calculate final confidence level
        confidence_level = self._calculate_confidence(state)
        
        # Build report
        report = IntelligenceReport(
            conversation_id=conversation_id,
            scam_type=state.scam_type,
            total_turns=state.turn_number,
            persona_used=state.persona,
            extracted_entities=state.extracted_entities,
            conversation_summary=summary,
            risk_score=state.risk_score,
            confidence_level=confidence_level,
            red_flags=red_flags,
            recommended_actions=recommended_actions,
            conversation_transcript=state.turns,
            created_at=state.created_at
        )
        
        return report
    
    def _merge_turn_entities(
        self,
        entities1: ExtractedEntities,
        entities2: ExtractedEntities
    ) -> ExtractedEntities:
        """Merge entities from two sources"""
        
        merged = ExtractedEntities()
        
        # Merge UPI IDs
        all_upi = set(entities1.upi_ids + entities2.upi_ids)
        merged.upi_ids = list(all_upi)
        
        # Merge phone numbers
        all_phones = set(entities1.phone_numbers + entities2.phone_numbers)
        merged.phone_numbers = list(all_phones)
        
        # Merge bank accounts
        all_accounts = entities1.bank_accounts + entities2.bank_accounts
        seen_accounts = set()
        unique_accounts = []
        for acc in all_accounts:
            if acc.account_number not in seen_accounts:
                seen_accounts.add(acc.account_number)
                unique_accounts.append(acc)
        merged.bank_accounts = unique_accounts
        
        # Merge URLs
        all_urls = set(entities1.phishing_links + entities2.phishing_links)
        merged.phishing_links = list(all_urls)
        
        # Merge aliases
        all_aliases = set(entities1.aliases + entities2.aliases)
        merged.aliases = list(all_aliases)
        
        # Merge organizations
        all_orgs = set(entities1.fake_organizations + entities2.fake_organizations)
        merged.fake_organizations = list(all_orgs)
        
        return merged
    
    def _convert_enhanced_entities(self, enhanced: dict) -> ExtractedEntities:
        """Convert enhanced entities (11 types) to old format"""
        from models.schemas import BankAccount
        
        entities = ExtractedEntities()
        
        # Map enhanced entities to old format
        entities.upi_ids = enhanced.get('upi_ids', [])
        entities.phone_numbers = enhanced.get('phone_numbers', [])
        entities.phishing_links = enhanced.get('phishing_links', [])
        entities.aliases = enhanced.get('names', [])  # Use names as aliases
        
        # Convert account numbers to BankAccount objects
        account_numbers = enhanced.get('account_numbers', [])
        ifsc_codes = enhanced.get('ifsc_codes', [])
        bank_names = enhanced.get('bank_names', [])
        
        for i, acc_num in enumerate(account_numbers):
            bank_account = BankAccount(
                account_number=acc_num,
                ifsc_code=ifsc_codes[i] if i < len(ifsc_codes) else None,
                bank_name=bank_names[i] if i < len(bank_names) else None
            )
            entities.bank_accounts.append(bank_account)
        
        return entities
    
    def _calculate_confidence(self, state) -> str:
        """Calculate confidence level based on extracted entities and conversation"""
        
        # Count extracted entities
        entity_count = (
            len(state.extracted_entities.upi_ids) +
            len(state.extracted_entities.bank_accounts) +
            len(state.extracted_entities.phishing_links) +
            len(state.extracted_entities.phone_numbers)
        )
        
        # High confidence: Multiple entities extracted, good risk score
        if entity_count >= 3 and state.risk_score >= 0.8:
            return "high"
        
        # Medium confidence: Some entities or decent risk score
        elif entity_count >= 1 or state.risk_score >= 0.6:
            return "medium"
        
        # Low confidence: Few entities, lower risk score
        else:
            return "low"
    
    def get_conversation_stats(self, conversation_id: str):
        """Get conversation statistics"""
        return self.conversation_manager.get_conversation_stats(conversation_id)
    
    def list_conversations(self):
        """List all conversations"""
        return self.conversation_manager.list_all_conversations()
