# ScamShield AI - Usage Guide

Learn how to use ScamShield AI to detect scams and extract intelligence.

---

## Getting Started

### 1. Start the Application

```bash
# From project root
start.bat
```

### 2. Access the Dashboard

Open your browser to: http://localhost:3000

### 3. Login

Click the **"🚀 Start Demo"** button on the login page.

> No credentials needed for demo mode!

---

## Core Features

### 🤖 Auto Demo Mode (Recommended)

The easiest way to see ScamShield AI in action:

1. Click **"Auto Demo Mode"** button on the dashboard
2. System automatically:
   - Selects a random scam scenario
   - Initiates conversation with scammer
   - Agent responds with humanized replies
   - Extracts intelligence in real-time
3. Stops automatically when:
   - 3+ entities extracted
   - Risk score > 80%
   - 20 conversation turns reached
4. Auto-exports data as JSON
5. Auto-emails report (if configured)

**Perfect for demos and testing!**

---

### 💬 Manual Conversation Mode

For more control over the interaction:

#### Starting a Conversation

1. **Use Quick Scenarios**:
   - Click any of the pre-defined scenario buttons
   - Examples: "Loan Approval", "Prize Winner", "Digital Arrest"

2. **Or Type Custom Message**:
   - Enter scammer message in the input field
   - Click "Send" or press Enter

#### During Conversation

- **Agent Response**: System automatically generates believable victim response
- **Intelligence Extraction**: Entities are extracted in real-time
- **Risk Assessment**: Risk score updates with each message
- **Phase Tracking**: Conversation phase shown (initial, engagement, extraction, exit)

#### Continuing the Conversation

1. Type the next scammer message
2. Click "Send"
3. Repeat until satisfied with intelligence gathered

---

## Understanding the Dashboard

### Left Panel: Conversation

- **Message History**: Full conversation transcript
- **Scammer Messages**: Shown in red/orange
- **Agent Messages**: Shown in blue/green
- **Input Field**: Type scammer messages here
- **Quick Scenarios**: Pre-defined scam templates

### Right Panel: Intelligence

#### Extracted Entities
Real-time display of extracted information:
- 📱 **Phone Numbers**
- 💳 **UPI IDs**
- 🏦 **Bank Accounts**
- 🔗 **Phishing Links**
- 👤 **Names**
- 📧 **Emails**
- 🏛️ **Bank Names**
- 🆔 **Aadhaar/PAN Numbers**

#### Risk Assessment
- **Risk Score**: 0-100% (updates in real-time)
- **Scam Type**: Detected scam category
- **Conversation Phase**: Current stage of interaction
- **Turn Count**: Number of message exchanges

---

## Advanced Features

### 📊 Analytics Dashboard

Navigate to **Analytics** page to view:

1. **Overall Metrics**:
   - Total scams handled
   - Entities extracted
   - Fraud prevented (estimated ₹)
   - Active conversations

2. **Charts**:
   - **Scam Distribution**: Pie chart of scam types
   - **Risk Trends**: 7-day trend analysis
   - **Entity Network**: Graph visualization (coming soon)

### 📚 Conversation History

Navigate to **History** page to:

1. **View Past Conversations**:
   - Search by content
   - Filter by date/scam type
   - Sort by risk score

2. **Review Details**:
   - Click any conversation to view full transcript
   - See all extracted entities
   - Review risk assessment

3. **Manage Conversations**:
   - Delete unwanted conversations
   - Export specific conversations

### 💾 Data Export

Multiple export formats available:

#### JSON Export
- Click **Download** button on dashboard
- Detailed structured data
- Includes all entities and metadata

#### CSV Export
- Navigate to **Data Export** page
- Click **Export CSV**
- Tabular format for spreadsheets

#### Excel Export
- Navigate to **Data Export** page
- Click **Export Excel**
- Formatted workbook with multiple sheets

#### Email Reports
- Click **Email** button on dashboard
- Requires SendGrid configuration
- Sends formatted intelligence report

---

## Understanding Scam Types

ScamShield AI detects and classifies these scam types:

### 1. Loan Approval Scams
- **Tactic**: Promise of instant loan approval
- **Goal**: Extract processing fees
- **Red Flags**: Upfront payment requests, too-good-to-be-true rates

### 2. Prize/Lottery Scams
- **Tactic**: Claim you've won a prize
- **Goal**: Get personal info or fees
- **Red Flags**: Unsolicited prizes, payment to claim

### 3. Digital Arrest Scams
- **Tactic**: Impersonate law enforcement
- **Goal**: Extort money through fear
- **Red Flags**: Threats, urgency, payment demands

### 4. Investment Scams
- **Tactic**: Promise high returns
- **Goal**: Steal investment money
- **Red Flags**: Guaranteed returns, pressure to invest quickly

### 5. Impersonation Scams
- **Tactic**: Pretend to be bank/government
- **Goal**: Steal credentials or money
- **Red Flags**: Requests for OTP, password, card details

---

## Best Practices

### For Effective Intelligence Gathering

1. **Let Conversations Develop**:
   - Don't rush to extract information
   - Build trust with scammer
   - Use humanized, believable responses

2. **Use Auto Demo Mode**:
   - Fully automated
   - Optimal conversation flow
   - Maximizes intelligence extraction

3. **Monitor Risk Score**:
   - Higher score = more dangerous scam
   - Stop when sufficient intelligence gathered
   - Export data before ending

4. **Review Extracted Entities**:
   - Verify accuracy
   - Cross-reference with conversation
   - Note patterns across conversations

### For Analysis

1. **Use Analytics Dashboard**:
   - Identify trending scam types
   - Track effectiveness over time
   - Spot patterns in scammer behavior

2. **Review History Regularly**:
   - Look for repeat scammers
   - Identify campaign patterns
   - Export data for law enforcement

3. **Export Data Frequently**:
   - Backup intelligence
   - Share with authorities
   - Maintain records

---

## Keyboard Shortcuts

- **Enter**: Send message
- **Ctrl + K**: Clear conversation
- **Ctrl + E**: Export JSON
- **Ctrl + A**: Start Auto Demo Mode

---

## Tips & Tricks

### Maximizing Intelligence Extraction

1. **Be Patient**: Let scammer reveal information naturally
2. **Show Interest**: Express eagerness to comply
3. **Ask Questions**: Request clarification on payment methods
4. **Build Trust**: Use persona-appropriate language
5. **Avoid Suspicion**: Don't ask too many direct questions

### Using Personas Effectively

The system uses 5+ personas:
- **Elderly Person**: Vulnerable, trusting, less tech-savvy
- **Young Professional**: Busy, interested in quick solutions
- **Student**: Limited funds, eager for opportunities
- **Homemaker**: Family-focused, cautious but hopeful
- **Small Business Owner**: Looking for financial solutions

Each persona has unique:
- Language patterns
- Response styles
- Vulnerability levels
- Trust thresholds

---

## Troubleshooting

### Conversation Not Starting
- **Check**: Backend server is running (http://localhost:8000)
- **Solution**: Restart backend with `python main.py`

### No Entities Extracted
- **Reason**: Scammer hasn't shared information yet
- **Solution**: Continue conversation, build trust

### Auto Demo Not Stopping
- **Reason**: Thresholds not met yet
- **Solution**: Wait or manually stop after 20 turns

### Export Not Working
- **Check**: Conversation has data to export
- **Solution**: Ensure conversation is active and has messages

---

## Next Steps

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Understand how the system works
- **[API.md](API.md)** - Integrate with other systems
- **[Archive](archive/)** - View development history

---

**Questions?** Check the archive for additional guides or create an issue on GitHub.
