# ScamShield AI - Quick Start Guide

## 🚀 How to Start ScamShield AI

### Option 1: Using start.bat (Recommended)

Simply double-click `start.bat` in the project root, or run:
```bash
start.bat
```

This will open two new command windows:
- **Backend Server** - Running on http://localhost:8000
- **Frontend Server** - Running on http://localhost:3000

### Option 2: Manual Start (If start.bat doesn't work)

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\python.exe main.py
```

**Terminal 2 - Frontend (in a new terminal):**
```bash
cd frontend
npm run dev
```

### Option 3: Using PowerShell

If you prefer PowerShell, create two terminals:

**Terminal 1:**
```powershell
cd backend
.\venv\Scripts\python.exe main.py
```

**Terminal 2:**
```powershell
cd frontend
npm run dev
```

---

## ✅ Verify It's Working

1. **Backend Check**: Open http://localhost:8000 in your browser
   - You should see: `{"status": "online", "service": "ScamShield AI"}`

2. **Frontend Check**: Open http://localhost:3000 in your browser
   - You should see the ScamShield AI dashboard

3. **API Docs**: Visit http://localhost:8000/docs
   - Interactive Swagger documentation

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError`
```bash
cd backend
venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Error**: `Port 8000 already in use`
```bash
# Find and kill the process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### Frontend Won't Start

**Error**: `npm not found`
- Install Node.js from https://nodejs.org/

**Error**: `Dependencies not installed`
```bash
cd frontend
npm install
```

**Error**: PowerShell execution policy
```bash
# Use cmd instead
cmd /c npm run dev
```

### start.bat Issues

If `start.bat` doesn't work, use **Option 2** (Manual Start) instead.

---

## 📝 Quick Reference

| What | URL |
|------|-----|
| Frontend Dashboard | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |

---

## 🎯 Next Steps

Once both servers are running:

1. Open http://localhost:3000
2. Click "🚀 Start Demo"
3. Try "Auto Demo Mode" for full automation
4. Or manually type scammer messages

For detailed usage, see [docs/USAGE.md](docs/USAGE.md)
