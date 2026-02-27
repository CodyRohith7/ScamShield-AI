from fastapi import APIRouter, Header, HTTPException, BackgroundTasks, Depends
from models.schemas import IncomingRequest, AgentResponse
from simple_agent import SimpleScamAgent
from services.callback_service import callback_service
import os

router = APIRouter()
agent = SimpleScamAgent()

# VALIDATE API KEY
async def verify_api_key(x_api_key: str = Header(None)):
    # Validate against the specific submission key
    expected_key = os.getenv("SUBMISSION_API_KEY", "your_submission_key_here")
    
    if not x_api_key or x_api_key != expected_key:
        raise HTTPException(status_code=403, detail="Invalid or Missing API Key")
    return x_api_key

@router.post("/api/chat", response_model=AgentResponse)
async def chat_endpoint(request: IncomingRequest, background_tasks: BackgroundTasks, x_api_key: str = Depends(verify_api_key)):

    """
    Main entry point for the Mock Scammer API.
    Strict Input/Output compliance.
    """
    try:
        # Extract content
        user_message = request.message.text
        session_id = request.sessionId
        
        # Convert Pydantic history to dict list
        history = [
            {"role": "scammer" if m.sender == "scammer" else "agent", "content": m.text}
            for m in request.conversationHistory
        ]
        
        # Generate Response
        result = agent.generate_response(user_message, history)
        reply = result.get("agent_response", "Error generating response")
        
        # Background: Send Callback if needed
        # We trigger callback if risk is high OR successful extraction
        if result.get("risk_score", 0) > 80 or result.get("entities"):
             background_tasks.add_task(
                 callback_service.send_report,
                 session_id,
                 history + [{"role": "agent", "content": reply}],
                 result.get("entities", {})
             )

        return {
            "status": "success",
            "reply": reply
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "reply": "Service temporarily unavailable"
        }
