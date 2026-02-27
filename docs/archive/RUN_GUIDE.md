# 🚀 HOW TO RUN SCAMSHIELD AI

**Quick Start Guide - Get Running in 5 Minutes!**

---

## 📋 PREREQUISITES

Make sure you have:
- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ npm or yarn installed

---

## 🔧 STEP 1: BACKEND SETUP

### **1.1 Open Terminal in Backend Directory**

```bash
cd c:\Users\codyr\.gemini\antigravity\scratch\scamshield-ai\backend
```

### **1.2 Create Virtual Environment (First Time Only)**

```bash
python -m venv venv
```

### **1.3 Activate Virtual Environment**

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

### **1.4 Install Dependencies**

```bash
pip install fastapi uvicorn python-dotenv pydantic sendgrid scikit-learn nltk numpy
```

### **1.5 Create .env File (Optional)**

Create `backend/.env` file:
```env
# Optional - for email functionality
SENDGRID_API_KEY=your_key_here

# Optional - for AI (uses rule-based if not set)
OPENAI_API_KEY=your_key_here
# OR
GEMINI_API_KEY=your_key_here
```

**Note**: The system works WITHOUT API keys using rule-based fallbacks!

### **1.6 Start Backend Server**

```bash
python main.py
```

**You should see**:
```
===========================================================
                                                            
                 SCAMSHIELD AI v2.0                       
                                                            
         Agentic Honey-Pot for Scam Detection                
         India AI Impact Buildathon 2026                      
                                                            
===========================================================

INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Backend is running on http://localhost:8000**

---

## 🎨 STEP 2: FRONTEND SETUP

### **2.1 Open NEW Terminal in Frontend Directory**

```bash
cd c:\Users\codyr\.gemini\antigravity\scratch\scamshield-ai\frontend
```

### **2.2 Install Dependencies (First Time Only)**

```bash
npm install
```

This will install:
- React
- Vite
- Tailwind CSS
- Framer Motion
- Recharts
- Axios
- React Router
- Zustand
- And more...

### **2.3 Start Frontend Dev Server**

```bash
npm run dev
```

**You should see**:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

✅ **Frontend is running on http://localhost:5173**

---

## 🌐 STEP 3: ACCESS THE APP

### **Open Your Browser**

Go to: **http://localhost:5173**

### **Login**

Use any credentials (demo mode):
- **Name**: Your Name
- **Email**: your@email.com
- **Role**: Security Analyst (or any)

Click **"Start Session"**

---

## 🎯 STEP 4: TRY AUTO DEMO MODE!

### **On Dashboard**:

1. **Select Scam Type** (dropdown at top)
   - Loan Approval Scam
   - Prize/Lottery Scam
   - Investment Scam
   - Digital Arrest Scam

2. **Click "Auto Mode" Button** 🚀

3. **Watch the Magic!**
   - System generates scammer message
   - Agent responds intelligently
   - Entities extracted in real-time
   - Conversation continues automatically
   - Stops when intelligence gathered
   - Auto-exports JSON
   - Auto-emails report (if configured)

---

## 📊 EXPLORE OTHER FEATURES

### **Analytics Page**
- View conversation statistics
- Risk score distribution
- Entity extraction charts
- Scam type breakdown

### **History Page**
- View all past conversations
- Search conversations
- Filter by scam type
- Export individual conversations
- Delete conversations

### **Campaigns Page**
- Click "Detect Campaigns"
- View ML-powered campaign clustering
- See campaign evolution
- Threat level assessment

### **Data Export Page**
- Export conversations as JSON/CSV
- Bulk export
- Email reports

---

## 🔍 VERIFY EVERYTHING WORKS

### **Test Backend API**

Open: **http://localhost:8000/docs**

You'll see Swagger UI with all 25+ endpoints!

Try:
- `GET /` - Health check
- `GET /api/health` - Detailed health
- `GET /api/mock-scammer/scenarios` - List scam scenarios

### **Test Frontend**

Navigate through all pages:
- ✅ Dashboard
- ✅ Analytics
- ✅ History
- ✅ Campaigns
- ✅ Data Export
- ✅ Settings
- ✅ Help
- ✅ About

---

## 🐛 TROUBLESHOOTING

### **Backend Won't Start**

**Error**: `ModuleNotFoundError`
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Error**: `Port 8000 already in use`
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in main.py (line 495)
uvicorn.run("main:app", host="0.0.0.0", port=8001, ...)
```

### **Frontend Won't Start**

**Error**: `npm not found`
```bash
# Install Node.js from nodejs.org
# Then run: npm install
```

**Error**: `Port 5173 already in use`
```bash
# Vite will automatically use next available port
# Or kill process on port 5173
```

### **Frontend Can't Connect to Backend**

**Check**:
1. Backend is running on http://localhost:8000
2. Frontend .env has correct API URL
3. No CORS errors in browser console

**Fix**:
Create `frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 📱 QUICK COMMANDS REFERENCE

### **Backend**
```bash
# Navigate
cd backend

# Activate venv
venv\Scripts\activate

# Run server
python main.py

# View logs
# (logs appear in terminal)
```

### **Frontend**
```bash
# Navigate
cd frontend

# Install deps
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🎬 DEMO WORKFLOW

### **Perfect Demo Flow**:

1. **Start Backend** (Terminal 1)
   ```bash
   cd backend
   venv\Scripts\activate
   python main.py
   ```

2. **Start Frontend** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open Browser**
   - Go to http://localhost:5173
   - Login with any credentials

4. **Run Auto Demo**
   - Select "Loan Approval Scam"
   - Click "Auto Mode"
   - Watch it run!

5. **Check Results**
   - View extracted entities
   - Check risk score
   - See conversation history

6. **Explore Features**
   - Go to Analytics
   - Go to History
   - Go to Campaigns (click "Detect Campaigns")
   - Export data

---

## 🏆 YOU'RE READY!

**Both servers running?** ✅  
**App accessible?** ✅  
**Auto demo works?** ✅  

**YOU'RE ALL SET! 🎉**

---

## 📞 NEED HELP?

### **Check**:
1. Both terminals are running
2. No error messages in terminals
3. Browser console (F12) has no errors
4. Correct URLs (localhost:8000 and localhost:5173)

### **Common Issues**:
- **Port conflicts**: Change ports in config
- **Module errors**: Reinstall dependencies
- **CORS errors**: Check backend CORS settings
- **API errors**: Check backend is running

---

<div align="center">

# 🚀 ENJOY YOUR SCAMSHIELD AI!

**Status**: ✅ RUNNING  
**Quality**: ⭐⭐⭐⭐⭐ PREMIUM  
**Ready**: 🎯 DEMO READY

**Go impress those judges! 🏆**

</div>
