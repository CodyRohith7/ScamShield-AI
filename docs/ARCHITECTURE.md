# ScamShield AI - Architecture

Technical architecture and system design documentation.

---

## System Overview

ScamShield AI is a multi-agent AI system designed to detect scams and extract intelligence through realistic conversations with scammers.

```
┌─────────────────────────────────────────────────────────────┐
│                     SCAMSHIELD AI v3.0                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Frontend   │◄──►│   Backend    │◄──►│   Database   │ │
│  │  React+Vite  │    │FastAPI+Uvicorn│   │   SQLite     │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                    │         │
│         │                    │                    │         │
│  ┌──────▼────────────────────▼────────────────────▼──────┐ │
│  │              Multi-Agent AI System                     │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │  • Persona Agent (5+ personas)                         │ │
│  │  • Detective Agent (scam classification)               │ │
│  │  • Intelligence Agent (entity extraction)              │ │
│  │  • Behavioral Fingerprinter                            │ │
│  │  • Language Mirror                                     │ │
│  │  • Tactic Analyzer                                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
- **React 18** - UI framework
- **Vite 7** - Build tool and dev server
- **React Router 6** - Client-side routing
- **Recharts** - Data visualization
- **Framer Motion** - Animations
- **Zustand** - State management
- **React Hot Toast** - Notifications
- **TailwindCSS** - Styling

### Backend
- **Python 3.10+** - Programming language
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **SQLite** - Database (in-memory)
- **python-dotenv** - Environment management

### AI/ML
- **OpenAI GPT-4** (optional) - LLM for enhanced responses
- **Google Gemini** (optional) - Alternative LLM
- **Rule-based System** - Fallback when no API keys
- **Scikit-learn** - ML utilities
- **NLTK** - Natural language processing

---

## Core Components

### 1. Agent Orchestrator

**Location**: `backend/core/orchestrator.py`

**Responsibilities**:
- Coordinates all agents
- Manages conversation flow
- Maintains conversation state
- Generates intelligence reports

**Key Methods**:
- `engage_with_scammer()` - Main entry point
- `generate_intelligence_report()` - Create final report
- `get_conversation_stats()` - Retrieve metrics

### 2. Detective Agent

**Location**: `backend/agents/detective_agent.py`

**Responsibilities**:
- Classify scam type
- Identify scam tactics
- Assess risk level
- Detect red flags

**Scam Types Detected**:
- Loan approval scams
- Prize/lottery scams
- Digital arrest scams
- Investment scams
- Impersonation scams

### 3. Persona Agent

**Location**: `backend/agents/persona_agent.py`

**Responsibilities**:
- Generate believable victim responses
- Maintain persona consistency
- Adapt to scammer's style
- Use 1000+ response variations

**Personas**:
- Elderly person
- Young professional
- Student
- Homemaker
- Small business owner

### 4. Intelligence Agent

**Location**: `backend/agents/intelligence_agent.py`

**Responsibilities**:
- Extract entities from messages
- Categorize extracted data
- Validate entity formats
- Track extraction progress

**Entities Extracted**:
- Phone numbers
- UPI IDs
- Bank accounts
- Phishing links
- Names
- Emails
- Bank names
- Aadhaar/PAN numbers

---

## Advanced Services

### 1. Behavioral Fingerprinting

**Location**: `backend/services/behavioral_fingerprinting.py`

**Purpose**: Identify same scammer across multiple conversations

**Features**:
- Response time patterns
- Message length distribution
- Vocabulary analysis
- Emoji usage patterns
- Aggression/urgency scoring

### 2. Language Mirroring

**Location**: `backend/services/language_mirroring.py`

**Purpose**: Adapt victim responses to match scammer's style

**Features**:
- Slang detection
- Emoji pattern matching
- Hinglish/regional language support
- Code word identification

### 3. Tactic Taxonomy

**Location**: `backend/services/tactic_taxonomy.py`

**Purpose**: Classify scammer manipulation tactics

**Tactics Detected**:
- Fear (threats, legal action)
- Urgency (limited time, act now)
- Authority (impersonation)
- Reward (prizes, returns)
- Scarcity (exclusive offers)
- Social proof (testimonials)

### 4. Campaign Detector

**Location**: `backend/services/campaign_detector.py`

**Purpose**: Identify coordinated fraud campaigns

**Features**:
- Script similarity analysis
- Pattern clustering
- Campaign lifecycle tracking
- Cross-conversation correlation

---

## Data Flow

### Conversation Flow

```
1. User/Scammer sends message
   ↓
2. Backend receives via /api/detect-and-engage
   ↓
3. Orchestrator coordinates agents:
   - Detective: Classify scam type
   - Persona: Generate response
   - Intelligence: Extract entities
   ↓
4. Response sent back to frontend
   ↓
5. Frontend updates UI:
   - Display message
   - Show extracted entities
   - Update risk score
   ↓
6. Repeat until conversation ends
```

### Data Storage

```
Conversation Data (In-Memory)
├── conversation_id
├── scam_type
├── risk_score
├── conversation_phase
├── messages[]
│   ├── role (scammer/agent)
│   ├── content
│   └── timestamp
├── extracted_entities{}
│   ├── upi_ids[]
│   ├── phone_numbers[]
│   ├── bank_accounts[]
│   └── ...
└── metadata{}
```

---

## API Architecture

### RESTful Endpoints

**Base URL**: `http://localhost:8000`

**Core Endpoints**:
- `POST /api/detect-and-engage` - Main conversation endpoint
- `GET /api/conversation/{id}` - Get conversation details
- `GET /api/conversations` - List all conversations
- `GET /api/analytics/metrics` - Get analytics

**Advanced Endpoints**:
- `POST /api/fingerprint/analyze` - Behavioral analysis
- `POST /api/language/mirror` - Language mirroring
- `POST /api/tactics/analyze` - Tactic detection
- `POST /api/campaigns/detect` - Campaign detection

See [API.md](API.md) for complete documentation.

---

## Security Considerations

### Data Protection
- No persistent storage of sensitive data
- In-memory database (cleared on restart)
- No logging of extracted entities
- API keys stored in .env (not committed)

### API Security
- CORS enabled for development
- Input validation via Pydantic
- Error handling prevents info leakage
- Rate limiting (planned)

### Ethical Considerations
- System designed for research/defense only
- Not for offensive scamming
- Intelligence shared with law enforcement
- Transparent about AI usage

---

## Scalability

### Current Limitations
- In-memory storage (not persistent)
- Single-server deployment
- No load balancing
- Limited to local deployment

### Future Enhancements
- PostgreSQL/MongoDB for persistence
- Redis for caching
- Kubernetes deployment
- Horizontal scaling
- CDN for frontend

---

## Performance

### Backend
- **Response Time**: < 500ms per message
- **Throughput**: ~100 requests/second
- **Memory**: ~200MB base + ~10MB per conversation

### Frontend
- **Load Time**: < 2 seconds
- **Bundle Size**: ~500KB (gzipped)
- **Render Performance**: 60fps animations

---

## Development Workflow

### Adding New Features

1. **Backend**:
   ```
   backend/
   ├── agents/          # Add new agents here
   ├── services/        # Add new services here
   ├── utils/           # Add utilities here
   └── models/schemas.py # Update data models
   ```

2. **Frontend**:
   ```
   frontend/src/
   ├── pages/           # Add new pages here
   ├── components/      # Add components here
   └── utils/           # Add utilities here
   ```

### Testing

**Backend**:
```bash
cd backend
python test_system.py
```

**Frontend**:
```bash
cd frontend
npm run dev
```

---

## Deployment

### Development
```bash
start.bat  # Runs both backend and frontend
```

### Production (Planned)
```bash
# Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
# Serve dist/ with nginx/apache
```

---

## Monitoring & Logging

### Current
- Console logging
- Error tracking in FastAPI
- Browser DevTools for frontend

### Planned
- Structured logging (JSON)
- Log aggregation (ELK stack)
- APM (Application Performance Monitoring)
- Alerting system

---

## Dependencies

### Backend
```
fastapi==0.128.0
uvicorn[standard]==0.40.0
pydantic==2.12.5
python-dotenv==1.2.1
scikit-learn==1.8.0
nltk==3.9.2
openai==2.16.0
google-generativeai==0.8.6
sendgrid==6.12.5
```

### Frontend
```
react@18.x
vite@7.x
react-router-dom@6.x
recharts@2.x
framer-motion@11.x
zustand@5.x
```

---

## Contributing

See main [README.md](../README.md) for contribution guidelines.

---

**Last Updated**: February 4, 2026
