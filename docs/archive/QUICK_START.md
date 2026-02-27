# ⚡ QUICK START - 30 SECONDS!

## 🚀 FASTEST WAY TO RUN

### **Option 1: Double-Click START.bat** (Easiest!)

1. **Double-click** `START.bat` in the project root
2. Two terminal windows will open automatically
3. Wait 10-15 seconds for servers to start
4. Open browser: **http://localhost:5173**
5. **DONE!** 🎉

---

### **Option 2: Manual Start** (If START.bat doesn't work)

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Then open**: http://localhost:5173

---

## 🎯 WHAT TO DO AFTER STARTING

### **1. Login**
- Use any name/email
- Click "Start Session"

### **2. Try Auto Demo Mode**
- Select scam type (dropdown)
- Click **"Auto Mode"** button
- Watch the magic! 🚀

### **3. Explore Features**
- **Dashboard** - Live conversations
- **Analytics** - Charts & stats
- **History** - Past conversations
- **Campaigns** - ML detection
- **Export** - Download data

---

## ✅ VERIFY IT'S WORKING

### **Backend Running?**
- Terminal shows: `Uvicorn running on http://0.0.0.0:8000`
- Visit: http://localhost:8000 (should show JSON)

### **Frontend Running?**
- Terminal shows: `Local: http://localhost:5173/`
- Visit: http://localhost:5173 (should show login page)

---

## 🐛 TROUBLESHOOTING

### **Dependencies Not Installed?**

**Backend:**
```bash
cd backend
pip install fastapi uvicorn python-dotenv pydantic sendgrid scikit-learn nltk numpy
```

**Frontend:**
```bash
cd frontend
npm install
```

### **Port Already in Use?**

**Kill process:**
```bash
# Find process
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# Kill it
taskkill /PID <PID> /F
```

### **Still Not Working?**

Check `RUN_GUIDE.md` for detailed instructions!

---

## 🎊 YOU'RE READY!

**Servers running?** ✅  
**Browser open?** ✅  
**Auto demo works?** ✅  

**GO WIN THAT BUILDATHON! 🏆**

---

## 📞 QUICK REFERENCE

| What | URL |
|------|-----|
| **Frontend** | http://localhost:5173 |
| **Backend** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

**Default Login**: Any name/email works!

---

<div align="center">

# 🛡️ SCAMSHIELD AI

**Status**: ✅ READY TO RUN  
**Time to Start**: ⚡ 30 seconds  
**Difficulty**: 🟢 EASY

**LET'S GO! 🚀**

</div>
