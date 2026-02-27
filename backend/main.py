from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
import os

from models.schemas import (
    EngageRequest, 
    EngageResponse, 
    IntelligenceReport,
    IncomingRequest,
    AgentResponse,
    ChatRequest
)
from core.orchestrator import AgentOrchestrator
from utils.mock_scammer import mock_scammer_api
from utils.email_service import email_service
from utils.data_export import data_export_service
from scam_templates import SCAM_TEMPLATES

# New advanced services
from database.conversation_db import conversation_db
from services.behavioral_fingerprinting import fingerprinter
from services.language_mirroring import language_mirror
from services.tactic_taxonomy import tactic_engine
from services.campaign_detector import campaign_detector
from utils.enhanced_entity_extractor import entity_extractor

# Load environment variables
load_dotenv()

# Global orchestrator instance
orchestrator: AgentOrchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global orchestrator
    
    # Startup
    print("[*] Starting ScamShield AI...")
    print(f"   OpenAI: {'[OK]' if os.getenv('OPENAI_API_KEY') else '[MISSING]'}")
    print(f"   Gemini: {'[OK]' if os.getenv('GEMINI_API_KEY') else '[MISSING]'}")
    
    orchestrator = AgentOrchestrator()
    print("[+] ScamShield AI ready!")
    
    yield
    
    # Shutdown
    print("[*] Shutting down ScamShield AI...")


# Create FastAPI app
app = FastAPI(
    title="ScamShield AI",
    description="Agentic Honey-Pot for Scam Detection & Intelligence Extraction",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "ScamShield AI",
        "version": "1.0.0",
        "description": "Agentic Honey-Pot for Scam Detection & Intelligence Extraction",
        "endpoints": {
            "engage": "POST /api/detect-and-engage",
            "report": "GET /api/conversation/{id}",
            "stats": "GET /api/conversation/{id}/stats",
            "list": "GET /api/conversations"
        }
    }


@app.post("/api/detect-and-engage", response_model=EngageResponse)
async def detect_and_engage(request: EngageRequest):
    """
    Main endpoint: Engage with scammer and extract intelligence
    
    This endpoint:
    1. Analyzes the scam message
    2. Generates a believable persona response
    3. Extracts fraud-related entities
    4. Returns structured intelligence
    """
    try:
        response = await orchestrator.engage_with_scammer(request)
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/conversation/{conversation_id}", response_model=IntelligenceReport)
async def get_intelligence_report(conversation_id: str):
    """
    Get complete intelligence report for a conversation
    
    Includes:
    - Full conversation transcript
    - All extracted entities
    - Risk assessment
    - Red flags identified
    - Recommended actions
    """
    try:
        report = await orchestrator.generate_intelligence_report(conversation_id)
        return report
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/conversation/{conversation_id}/stats")
async def get_conversation_stats(conversation_id: str):
    """Get statistics about a conversation"""
    try:
        stats = orchestrator.get_conversation_stats(conversation_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/conversations")
async def list_conversations():
    """List all conversations"""
    try:
        conversations = orchestrator.list_conversations()
        return {
            "total": len(conversations),
            "conversations": conversations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "ai_providers": {
            "openai": "configured" if os.getenv("OPENAI_API_KEY") else "not configured",
            "gemini": "configured" if os.getenv("GEMINI_API_KEY") else "not configured"
        },
        "agents": {
            "detective": "active",
            "persona": "active",
            "intelligence": "active"
        },
        "orchestrator": "active"
    }


# ============================================================================
# COMPATIBILITY ENDPOINTS (Supporting frontend /api/chat)
# ============================================================================

@app.post("/api/chat", response_model=AgentResponse)
async def chat_compat(request: ChatRequest):
    """
    Unified chat endpoint for frontend compatibility.
    Uses the advanced orchestrator under the hood.
    """
    print(f"[*] Incoming chat message: {request.message[:50]}...")
    try:
        # Convert ChatRequest to EngageRequest
        engage_request = EngageRequest(
            message=request.message,
            conversation_id=request.sessionId if request.sessionId and request.sessionId != "new" else None
        )
        
        # Engage with orchestrator
        response = await orchestrator.engage_with_scammer(engage_request)
        
        return {
            "status": "success",
            "reply": response.agent_response,
            "conversation_id": response.conversation_id,
            "scam_type": response.scam_type,
            "persona_used": response.persona_used,
            "risk_score": response.risk_score,
            "turn_number": response.turn_number,
            "entities": response.extracted_entities,
            "internal_reasoning": response.internal_reasoning
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "reply": f"Sorry, I encountered an error: {str(e)}"
        }


@app.get("/api/scam-templates")
async def list_scam_templates():
    """List all available scam templates for demo mode"""
    templates = []
    for tid, data in SCAM_TEMPLATES.items():
        templates.append({
            "id": tid,
            "name": data["name"],
            "description": data["description"],
            "scam_type": data["scam_type"],
            "message_count": len(data["messages"])
        })
    return {"templates": templates}


@app.get("/api/scam-template/{template_id}")
async def get_scam_template(template_id: str):
    """Get a specific scam template"""
    template = SCAM_TEMPLATES.get(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


# ============================================================================
# ENHANCED ENDPOINTS - Mock Scammer, Email, Export
# ============================================================================

@app.get("/api/mock-scammer/scenarios")
async def list_scam_scenarios():
    """List all available scam scenarios for testing"""
    try:
        scenarios = mock_scammer_api.list_all_scam_types()
        return {
            "total": len(scenarios),
            "scenarios": scenarios
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/mock-scammer/generate")
async def generate_scammer_response(request: dict):
    """
    Generate realistic scammer response for testing
    
    Request body:
    {
        "victim_message": str,
        "scam_type": str,
        "turn_number": int,
        "conversation_history": list (optional)
    }
    """
    try:
        response = mock_scammer_api.generate_scammer_response(
            victim_message=request.get("victim_message", ""),
            conversation_history=request.get("conversation_history", []),
            scam_type=request.get("scam_type", "loan_approval"),
            turn_number=request.get("turn_number", 1)
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/email/send-report/{conversation_id}")
async def send_email_report(conversation_id: str, recipients: list = None):
    """Send intelligence report via email"""
    try:
        # Get the report
        report = await orchestrator.generate_intelligence_report(conversation_id)
        
        # Send email
        success = await email_service.send_intelligence_report(
            conversation_id=conversation_id,
            report_data=report.dict(),
            recipients=recipients
        )
        
        return {
            "success": success,
            "message": "Email sent successfully" if success else "Email service not configured"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/export/pdf/{conversation_id}")
async def export_pdf_report(conversation_id: str):
    """Export intelligence report as PDF"""
    try:
        # Get the report
        report = await orchestrator.generate_intelligence_report(conversation_id)
        
        # Generate PDF
        pdf_buffer = data_export_service.generate_pdf_report(report.dict())
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=scamshield_report_{conversation_id}.pdf"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/export/json/{conversation_id}")
async def export_json_report(conversation_id: str):
    """Export intelligence report as JSON"""
    try:
        # Get the report
        report = await orchestrator.generate_intelligence_report(conversation_id)
        
        # Generate JSON
        json_data = data_export_service.generate_json_export(report.dict())
        
        return StreamingResponse(
            iter([json_data]),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=scamshield_report_{conversation_id}.json"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/export/csv")
async def export_csv_all_conversations():
    """Export all conversations as CSV"""
    try:
        # Get all conversations
        conversations = orchestrator.list_conversations()
        
        # Generate CSV
        csv_buffer = data_export_service.generate_csv_export(conversations)
        
        return StreamingResponse(
            csv_buffer,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=scamshield_conversations.csv"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/export/excel")
async def export_excel_all_conversations():
    """Export all conversations as Excel"""
    try:
        # Get all conversations
        conversations = orchestrator.list_conversations()
        
        # Generate Excel
        excel_buffer = data_export_service.generate_excel_export(conversations)
        
        return StreamingResponse(
            excel_buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=scamshield_conversations.xlsx"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/api/analytics/metrics")
async def get_analytics_metrics():
    """Get overall analytics metrics"""
    try:
        conversations = orchestrator.list_conversations()
        
        # Calculate metrics
        total_scams = len(conversations)
        total_entities = 0
        total_risk = 0
        active_conversations = 0
        
        for conv in conversations:
            entities = conv.get('extracted_entities', {})
            total_entities += (
                len(entities.get('upi_ids', [])) +
                len(entities.get('phone_numbers', [])) +
                len(entities.get('bank_accounts', [])) +
                len(entities.get('phishing_links', []))
            )
            total_risk += conv.get('risk_score', 0)
            if conv.get('conversation_phase') not in ['exit', 'completed']:
                active_conversations += 1
        
        avg_risk = total_risk / total_scams if total_scams > 0 else 0
        fraud_prevented = total_scams * 25000  # Estimated ₹25k per scam
        
        return {
            "totalScamsHandled": total_scams,
            "entitiesExtracted": total_entities,
            "fraudPrevented": fraud_prevented,
            "activeConversations": active_conversations,
            "avgRiskScore": avg_risk
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/analytics/trends")
async def get_analytics_trends(period: str = "7d"):
    """Get trend data for specified period"""
    try:
        # Mock trend data for now
        # In production, this would query a time-series database
        import random
        from datetime import datetime, timedelta
        
        days = int(period.replace('d', ''))
        trends = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            trends.append({
                "date": date.strftime("%Y-%m-%d"),
                "scams": random.randint(5, 20),
                "entities": random.randint(10, 40),
                "riskScore": random.randint(50, 90)
            })
        
        return {"trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/analytics/network-graph")
async def get_network_graph():
    """Get network graph data for entity relationships"""
    try:
        conversations = orchestrator.list_conversations()
        
        nodes = []
        edges = []
        node_ids = set()
        
        for conv in conversations:
            conv_id = conv.get('conversation_id', '')
            entities = conv.get('extracted_entities', {})
            
            # Add conversation node
            if conv_id not in node_ids:
                nodes.append({
                    "id": conv_id,
                    "type": "conversation",
                    "label": f"Conv {conv_id[:8]}",
                    "scamType": conv.get('scam_type', 'unknown')
                })
                node_ids.add(conv_id)
            
            # Add entity nodes and edges
            for upi in entities.get('upi_ids', []):
                if upi not in node_ids:
                    nodes.append({"id": upi, "type": "upi", "label": upi})
                    node_ids.add(upi)
                edges.append({"source": conv_id, "target": upi, "type": "has_upi"})
            
            for phone in entities.get('phone_numbers', []):
                if phone not in node_ids:
                    nodes.append({"id": phone, "type": "phone", "label": phone})
                    node_ids.add(phone)
                edges.append({"source": conv_id, "target": phone, "type": "has_phone"})
        
        return {"nodes": nodes, "edges": edges}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/api/analytics/scam-distribution")
async def get_scam_distribution():
    """Get scam type distribution"""
    try:
        conversations = orchestrator.list_conversations()
        
        distribution = {}
        for conv in conversations:
            scam_type = conv.get('scam_type', 'unknown')
            distribution[scam_type] = distribution.get(scam_type, 0) + 1
        
        result = [
            {"name": k.replace('_', ' ').title(), "value": v}
            for k, v in distribution.items()
        ]
        
        return {"distribution": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# ============================================================================
# ADVANCED FEATURES - v3.0
# ============================================================================

@app.get("/api/history/conversations")
async def get_conversation_history(limit: int = 100, offset: int = 0):
    """Get conversation history with pagination"""
    try:
        conversations = conversation_db.list_conversations(limit=limit, offset=offset)
        stats = conversation_db.get_statistics()
        return {
            "conversations": conversations,
            "total": stats.get('total_conversations', 0),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/conversation/{conversation_id}")
async def get_conversation_from_history(conversation_id: str):
    """Get specific conversation from history"""
    try:
        conversation = conversation_db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/history/conversation/{conversation_id}")
async def delete_conversation_from_history(conversation_id: str, hard_delete: bool = False):
    """Delete conversation from history"""
    try:
        success = conversation_db.delete_conversation(conversation_id, hard_delete)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return {"success": True, "message": "Conversation deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/search")
async def search_conversation_history(query: str):
    """Search conversations by content"""
    try:
        results = conversation_db.search_conversations(query)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/statistics")
async def get_history_statistics():
    """Get conversation history statistics"""
    try:
        stats = conversation_db.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fingerprint/analyze")
async def analyze_behavioral_fingerprint(request: dict):
    """
    Analyze behavioral fingerprint of a conversation
    
    Request body:
    {
        "conversation_id": str,
        "conversation": dict (optional, if not in DB)
    }
    """
    try:
        conversation_id = request.get("conversation_id")
        conversation = request.get("conversation")
        
        if not conversation:
            # Try to get from database
            conversation = conversation_db.get_conversation(conversation_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Extract fingerprint
        fingerprint = fingerprinter.extract_fingerprint(conversation)
        
        # Try to match with known scammers
        match_result = fingerprinter.match_fingerprint(fingerprint)
        
        return {
            "conversation_id": conversation_id,
            "fingerprint": fingerprint,
            "match_result": match_result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fingerprint/register")
async def register_scammer_fingerprint(request: dict):
    """
    Register a new scammer fingerprint
    
    Request body:
    {
        "scammer_id": str,
        "fingerprint": dict
    }
    """
    try:
        scammer_id = request.get("scammer_id")
        fingerprint = request.get("fingerprint")
        
        if not scammer_id or not fingerprint:
            raise HTTPException(status_code=400, detail="Missing scammer_id or fingerprint")
        
        fingerprinter.register_fingerprint(scammer_id, fingerprint)
        
        return {
            "success": True,
            "message": f"Scammer {scammer_id} registered"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/language/mirror")
async def mirror_language_style(request: dict):
    """
    Mirror scammer's language in a response
    
    Request body:
    {
        "base_response": str,
        "scammer_messages": list,
        "intensity": float (0-1, default 0.5)
    }
    """
    try:
        base_response = request.get("base_response", "")
        scammer_messages = request.get("scammer_messages", [])
        intensity = request.get("intensity", 0.5)
        
        if not base_response:
            raise HTTPException(status_code=400, detail="Missing base_response")
        
        # Learn from scammer messages
        if scammer_messages:
            language_mirror.learn_from_conversation(scammer_messages)
        
        # Mirror language
        mirrored_response = language_mirror.mirror_language(base_response, intensity)
        
        # Get style summary
        style_summary = language_mirror.get_style_summary()
        
        return {
            "original_response": base_response,
            "mirrored_response": mirrored_response,
            "style_summary": style_summary
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/tactics/analyze")
async def analyze_scammer_tactics(request: dict):
    """
    Analyze scammer tactics in a message or conversation
    
    Request body:
    {
        "message": str (for single message),
        OR
        "messages": list (for full conversation)
    }
    """
    try:
        message = request.get("message")
        messages = request.get("messages")
        
        if message:
            # Analyze single message
            detections = tactic_engine.analyze_message(message)
            return {
                "message": message,
                "tactics_detected": [
                    {
                        "tactic": d.tactic,
                        "confidence": d.confidence,
                        "keywords": d.keywords_matched,
                        "description": tactic_engine.get_tactic_description(d.tactic),
                        "counter_strategy": tactic_engine.get_counter_strategy(d.tactic)
                    }
                    for d in detections
                ]
            }
        elif messages:
            # Analyze full conversation
            analysis = tactic_engine.analyze_conversation(messages)
            return analysis
        else:
            raise HTTPException(status_code=400, detail="Missing message or messages")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tactics/report/{conversation_id}")
async def get_tactic_report(conversation_id: str):
    """Get tactic analysis report for a conversation"""
    try:
        conversation = conversation_db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = conversation.get("messages", [])
        analysis = tactic_engine.analyze_conversation(messages)
        report = tactic_engine.export_analysis(analysis)
        
        return {
            "conversation_id": conversation_id,
            "analysis": analysis,
            "report": report
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/campaigns/detect")
async def detect_fraud_campaigns(request: dict):
    """
    Detect fraud campaigns from conversations
    
    Request body:
    {
        "conversation_ids": list (optional, uses all if not provided),
        "similarity_threshold": float (default 0.7),
        "min_conversations": int (default 2)
    }
    """
    try:
        conversation_ids = request.get("conversation_ids")
        similarity_threshold = request.get("similarity_threshold", 0.7)
        min_conversations = request.get("min_conversations", 2)
        
        # Get conversations
        if conversation_ids:
            conversations = [conversation_db.get_conversation(cid) for cid in conversation_ids]
            conversations = [c for c in conversations if c]  # Filter None
        else:
            # Get all conversations
            conversations = conversation_db.list_conversations(limit=1000)
        
        if len(conversations) < min_conversations:
            return {
                "campaigns": [],
                "message": f"Not enough conversations (need at least {min_conversations})"
            }
        
        # Detect campaigns
        campaigns = campaign_detector.detect_campaigns(
            conversations,
            similarity_threshold,
            min_conversations
        )
        
        return {
            "campaigns": campaigns,
            "total_campaigns": len(campaigns),
            "conversations_analyzed": len(conversations)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/campaigns/active")
async def get_active_campaigns():
    """Get all active fraud campaigns"""
    try:
        campaigns = campaign_detector.list_active_campaigns()
        return {
            "active_campaigns": campaigns,
            "count": len(campaigns)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/campaigns/statistics")
async def get_campaign_statistics():
    """Get campaign statistics"""
    try:
        stats = campaign_detector.get_campaign_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/campaigns/report/{campaign_id}")
async def get_campaign_report(campaign_id: str):
    """Get detailed campaign report"""
    try:
        campaign = campaign_detector.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        report = campaign_detector.export_campaign_report(campaign_id)
        
        return {
            "campaign": campaign,
            "report": report
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/entities/extract")
async def extract_entities_from_text(request: dict):
    """
    Extract entities from text
    
    Request body:
    {
        "text": str,
        OR
        "messages": list
    }
    """
    try:
        text = request.get("text")
        messages = request.get("messages")
        
        if text:
            entities = entity_extractor.extract_all(text)
            validated = entity_extractor.validate_entities(entities)
            return validated.to_dict()
        elif messages:
            entities = entity_extractor.extract_from_conversation(messages)
            validated = entity_extractor.validate_entities(entities)
            return validated.to_dict()
        else:
            raise HTTPException(status_code=400, detail="Missing text or messages")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Resource not found", "detail": str(exc)}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
    ===========================================================
                                                           
                 SCAMSHIELD AI v2.0                       
                                                           
         Agentic Honey-Pot for Scam Detection                
         India AI Impact Buildathon 2026                      
                                                           
    ===========================================================
    """)
    
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        print("WARNING: No AI API keys configured!")
        print("   Set OPENAI_API_KEY or GEMINI_API_KEY in .env file")
        print("   System will use rule-based fallbacks\n")
    
    # Run server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
