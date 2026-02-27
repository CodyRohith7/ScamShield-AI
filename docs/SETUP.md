# ScamShield AI - Setup Guide

Complete installation and configuration guide for ScamShield AI.

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.10+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/scamshield-ai.git
cd scamshield-ai
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

---

## Configuration

### Environment Variables (Optional)

The system works **perfectly without API keys** using a rule-based fallback system. However, for enhanced AI capabilities, you can configure:

1. Copy the example environment file:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```env
   # OpenAI (Optional - for enhanced AI responses)
   OPENAI_API_KEY=your_openai_key_here
   
   # Google Gemini (Optional - alternative to OpenAI)
   GEMINI_API_KEY=your_gemini_key_here
   
   # SendGrid (Optional - for email reports)
   SENDGRID_API_KEY=your_sendgrid_key_here
   FROM_EMAIL=your_email@example.com
   OWNER_EMAIL=recipient@example.com
   ```

### Getting API Keys (Optional)

- **OpenAI**: https://platform.openai.com/api-keys
- **Google Gemini**: https://makersuite.google.com/app/apikey
- **SendGrid**: https://sendgrid.com/

---

## Running the Application

### Option 1: Quick Start (Recommended)

From the project root directory:

```bash
start.bat
```

This will automatically:
- Start the backend server on http://localhost:8000
- Start the frontend server on http://localhost:3000 (or next available port)
- Open your browser

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
.\venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## Verification

### 1. Check Backend Health

Open your browser to: http://localhost:8000

You should see:
```json
{
  "status": "online",
  "service": "ScamShield AI",
  "version": "1.0.0"
}
```

### 2. Check API Documentation

Visit: http://localhost:8000/docs

You should see the interactive Swagger API documentation.

### 3. Check Frontend

Visit: http://localhost:3000 (or the port shown in your terminal)

You should see the ScamShield AI dashboard.

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
```bash
# Solution: Ensure virtual environment is activated and dependencies installed
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Problem**: Port 8000 already in use
```bash
# Solution: Kill the process or change port in main.py
# Find and kill process on Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### Frontend Issues

**Problem**: `npm: command not found`
```bash
# Solution: Install Node.js from https://nodejs.org/
```

**Problem**: Port 3000 already in use
```bash
# Solution: Vite will automatically use next available port
# Check terminal output for actual port number
```

### API Key Issues

**Problem**: "API key not configured" warnings
```
# Solution: This is normal! The system works without API keys.
# If you want AI-enhanced responses, add keys to backend/.env
```

---

## Next Steps

Once installed, proceed to:
- **[USAGE.md](USAGE.md)** - Learn how to use ScamShield AI
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Understand the system architecture
- **[API.md](API.md)** - Explore API endpoints

---

## System Requirements

### Minimum
- **CPU**: Dual-core processor
- **RAM**: 4GB
- **Disk**: 500MB free space
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 20.04+

### Recommended
- **CPU**: Quad-core processor
- **RAM**: 8GB
- **Disk**: 1GB free space
- **OS**: Windows 11, macOS 12+, Ubuntu 22.04+

---

**Need Help?** Check the [archive](archive/) for additional troubleshooting guides or create an issue on GitHub.
