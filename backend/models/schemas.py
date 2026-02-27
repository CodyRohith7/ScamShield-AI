from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any, Union
from enum import Enum
from datetime import datetime

class ScamType(str, Enum):
    LOAN_SCAM = "loan_approval"
    PRIZE_SCAM = "prize_lottery"
    INVESTMENT_FRAUD = "investment_opportunity"
    JOB_SCAM = "fake_job_offer"
    TECH_SUPPORT = "technical_support"
    CRYPTOCURRENCY = "cryptocurrency_fraud"
    OTHER = "other"

class PersonaType(str, Enum):
    CAUTIOUS_MIDDLE_AGED = "cautious_middle_aged"
    EAGER_YOUNG_ADULT = "eager_young_adult"
    BUSY_PROFESSIONAL = "busy_professional"
    SENIOR_CITIZEN = "senior_citizen"
    TECH_SAVVY_STUDENT = "tech_savvy_student"

class ConversationPhase(str, Enum):
    TRUST_BUILDING = "trust_building"
    INFORMATION_GATHERING = "information_gathering"
    INTELLIGENCE_EXTRACTION = "intelligence_extraction"
    SAFE_EXIT = "safe_exit"
    EXIT = "exit"
    COMPLETED = "completed"

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

class BankAccount(BaseModel):
    account_number: str
    ifsc: Optional[str] = None
    ifsc_code: Optional[str] = None
    bank_name: Optional[str] = None
    confidence: float = 1.0

class ExtractedEntities(BaseModel):
    upi_ids: List[str] = []
    phone_numbers: List[str] = []
    bank_accounts: List[BankAccount] = []
    phishing_links: List[str] = []
    aliases: List[str] = []
    fake_organizations: List[str] = []

class ConversationTurn(BaseModel):
    turn_number: int
    scammer_message: str
    agent_response: str
    timestamp: datetime = Field(default_factory=datetime.now)
    entities_extracted: ExtractedEntities
    internal_reasoning: Optional[str] = ""

class ConversationState(BaseModel):
    conversation_id: str
    scam_type: ScamType
    persona: PersonaType
    phase: ConversationPhase
    turn_number: int
    turns: List[ConversationTurn] = []
    extracted_entities: ExtractedEntities
    risk_score: float = 0.0
    context_summary: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class EngageRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class EngageResponse(BaseModel):
    conversation_id: str
    agent_response: str
    scam_type: ScamType
    persona_used: PersonaType
    conversation_phase: ConversationPhase
    turn_number: int
    extracted_entities: Union[ExtractedEntities, Dict[str, Any]]
    risk_score: float
    confidence_level: str
    internal_reasoning: Optional[str] = None
    should_continue: bool = True

class IntelligenceReport(BaseModel):
    conversation_id: str
    scam_type: ScamType
    total_turns: int
    persona_used: PersonaType
    extracted_entities: Union[ExtractedEntities, Dict[str, Any]]
    conversation_summary: str
    risk_score: float
    confidence_level: str
    red_flags: List[str] = []
    recommended_actions: List[str] = []
    conversation_transcript: List[Any] = []
    created_at: datetime = Field(default_factory=datetime.now)

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[dict] = []
    sessionId: Optional[str] = None

class IncomingRequest(BaseModel):
    sessionId: str
    message: dict
    conversationHistory: List[dict] = []
    metadata: Optional[dict] = None

class AgentResponse(BaseModel):
    status: Literal["success", "error"]
    reply: str
