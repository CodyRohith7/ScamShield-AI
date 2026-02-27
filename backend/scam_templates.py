"""
Scam templates for Test Demo Mode
Pre-built scammer conversation scripts for testing the honeypot agent
"""

SCAM_TEMPLATES = {
    "instant_loan": {
        "name": "💰 Instant Loan Scam",
        "description": "Advance fee fraud targeting people needing urgent money",
        "scam_type": "loan_approval",
        "messages": [
            "Hello! Congratulations! Your loan application has been PRE-APPROVED by QuickCash Financial Services. You are eligible for instant personal loan of ₹2,50,000 at just 9.5% interest rate. No documents required. Money will be transferred within 2 hours. This is limited time offer. Are you interested?",
            
            "Sir, this is 100% genuine offer from RBI approved NBFC. We have already disbursed ₹450 crores to 85,000+ customers across India. Your CIBIL score is good that's why you got pre-approved. Process is very simple: 1. Pay one-time processing fee ₹999 2. Loan approved immediately 3. Amount credited to your account in 1-2 hours. No hidden charges. No documentation needed. Would you like to proceed?",
            
            "Sir, I understand your concern. But this offer is valid only for TODAY. After 6 PM, interest rate will increase to 14.5% and processing fee will be ₹2,499. We have only 12 slots remaining for today. If you want to save money, please confirm now. Thousands of people are applying right now. Don't miss this golden opportunity!",
            
            "Great decision sir! For processing fee payment, please send ₹999 to this UPI ID: quickcash.loans@paytm. After payment, please share screenshot on WhatsApp: 9876543210. Your Loan Reference Number is: QL2026789012. Within 2 hours, ₹2,50,000 will be credited to your account. Our legal team will send loan agreement on your email. Thank you for choosing QuickCash!",
            
            "Sir, I completely understand your concern about UPI payment. Actually our payment gateway is under maintenance today, that's why we are using backup UPI method. If you want, I can also give you our bank account details: Account Name: Rajesh Kumar, Account Number: 50100298765432, IFSC Code: HDFC0001234, Bank: HDFC Bank, Mumbai. This is our company director's account. You can verify our company registration number: U65999MH2015PTC268945."
        ]
    },
    
    "lottery_prize": {
        "name": "🎉 Lottery Prize Scam",
        "description": "Lucky draw winner scam targeting general public",
        "scam_type": "prize_lottery",
        "messages": [
            "🎉🎉 CONGRATULATIONS 🎉🎉 Dear Customer, Your mobile number has been selected as WINNER in Big Bazaar 25th Anniversary Lucky Draw! You have WON: ₹5,00,000 (Five Lakh Rupees) + iPhone 15 Pro Max + Gold Coin (10 grams). This is 100% GENUINE. Your Lucky Draw Ticket Number: BB-2026-789456. To claim your prize, please reply YES immediately!",
            
            "Thank you for your interest! You are very lucky person! Out of 10 crore participants, only 100 winners were selected and you are one of them! Your Prize Amount: ₹5,00,000 + iPhone 15 Pro Max + 10gm Gold Coin. Total Value: ₹7,89,000. Official Website: www.bigbazaar-winners.tk. For verification, please provide: 1. Your full name 2. Your complete address 3. PAN card number 4. Email ID. This information is needed for prize distribution and income tax purpose.",
            
            "Great! Your details have been verified successfully. Now for prize claim process, you need to pay one-time processing fee of ₹5,000. This includes: Government Tax (GST) - ₹2,000, Prize Processing Charges - ₹1,500, Courier Delivery Charges - ₹1,000, Certificate Charges - ₹500. Total: ₹5,000 only. After payment, your prize will be couriered to your address within 5-7 working days.",
            
            "To complete payment of ₹5,000, please use UPI ID: bigbazaar.prize@paytm. After payment, WhatsApp screenshot to: 98765-43210. Your prize will be dispatched same day! Alternatively you can transfer to Bank Account: Account Name: Big Bazaar Prize Distribution, Account No: 918765432109876, IFSC: SBIN0012345",
            
            "⚠️ IMPORTANT NOTICE - Our system shows you have not completed payment yet. Please note: Prize claim deadline: Today 11:59 PM. After deadline, prize will go to next standby winner. You will lose ₹7,89,000 worth prizes. This is FINAL REMINDER. Don't miss this lifetime opportunity! Pay ₹5,000 now!"
        ]
    },
    
    "investment_trading": {
        "name": "📈 Investment Scam",
        "description": "Ponzi scheme promising guaranteed stock market returns",
        "scam_type": "investment",
        "messages": [
            "Hello Sir/Madam! I am calling from WEALTH CREATORS Investment Advisory Services. We are SEBI registered stock market experts with 15 years experience. We provide guaranteed monthly returns through our AI-powered trading algorithm! Our track record: 2,500+ satisfied investors, Average returns: 25% per month, Zero loss guarantee, Minimum investment: ₹10,000 only. Would you be interested to know more about this opportunity?",
            
            "Excellent! Let me explain our revolutionary system: We use Artificial Intelligence to predict stock market with 94.7% accuracy! GOLD Plan: Investment ₹25,000, Monthly Return: 25% (₹6,250/month), Total in 1 year: ₹1,00,000 (Net profit ₹75,000). PLATINUM Plan: Investment ₹50,000, Monthly Return: 30% (₹15,000/month), Total in 1 year: ₹2,30,000 (Net profit ₹1,80,000). Which plan suits you?",
            
            "Great choice sir! Let me show you real results: Ramesh Kumar (Delhi) - Invested ₹25,000 in Jan 2025, Current value: ₹78,000 (in just 3 months!). Priya Singh (Bangalore) - Invested ₹50,000 in Dec 2024, Current value: ₹1,65,000 (in just 4 months!). I can connect you with these customers if you want to verify! We also have WhatsApp group of 500+ investors where daily profit updates are shared.",
            
            "Perfect sir! To activate your GOLD Plan (₹25,000 investment), please make payment: UPI ID: wealth.invest@ybl OR Account Name: Wealth Creators Pvt Ltd, Account Number: 234567890123, IFSC: ICIC0001234. Share payment screenshot on WhatsApp: 98765-43210. Your trading account will be activated within 2 hours. From next month, ₹6,250 will be credited to your bank account on 1st of every month!",
            
            "🎯 SPECIAL ANNOUNCEMENT - FLASH SALE for next 2 hours only! If you invest NOW, you get: BONUS 5% extra returns (Total 30% monthly instead of 25%), FREE lifetime membership (Worth ₹5,000), Priority customer support. This offer ends at 6 PM today! Only 8 slots remaining! Don't miss this! Invest ₹25,000 NOW and start getting ₹7,500 per month!"
        ]
    },
    
    "kyc_update": {
        "name": "🏦 KYC Update Scam",
        "description": "Banking fraud targeting account holders",
        "scam_type": "impersonation",
        "messages": [
            "⚠️ IMPORTANT SECURITY ALERT - This is automated message from State Bank of India. Dear Customer, Your account KYC (Know Your Customer) has EXPIRED as per RBI guidelines. Account Number: XXXX-XXXX-8765. Your account will be BLOCKED within 24 hours if KYC not updated immediately! To update KYC instantly and avoid account blocking, reply UPDATE now. - SBI Security Team",
            
            "Thank you for responding! As per RBI new guidelines, all bank accounts must update KYC details. Your Account Status: CRITICAL. Pending Items: Aadhaar linking, PAN verification, Mobile number update. If not updated by TONIGHT 11:59 PM: Account will be FROZEN, ATM card BLOCKED, Internet banking DISABLED. Our KYC Officer will call you shortly. Please keep ready: Your ATM/Debit card, Mobile phone, PAN card.",
            
            "Hello, this is Rahul Verma from State Bank of India Central KYC Department. Your SBI account has been flagged for KYC expiry. For security verification, please confirm: 1. Your date of birth 2. Your registered mobile number 3. Last 4 digits of your ATM card. I can see multiple issues in your account: Aadhaar linking pending, Email not verified, Address proof expired. Don't worry, I will resolve everything right now!",
            
            "Perfect! For KYC update, I need to verify your card in our system. Please tell me: 1. Card holder name 2. 16-digit card number 3. Expiry date (MM/YY) 4. 3-digit CVV number. Sir/Madam, I am calling from bank only! This is secure line! I need these details to verify your card is genuine! Your account blocking timer is running! Please share details fast!",
            
            "Thank you! System is sending OTP to your mobile for final verification. You will receive 6-digit OTP SMS in few seconds from SBI. Once you receive OTP, please read it out immediately! We have only 3 minutes before it expires! Sir/Ma'am, I am from BANK! I need OTP to complete your KYC! If you don't share OTP, your account will be blocked permanently! What is the 6-digit number you received?"
        ]
    }
}


def get_template(template_id):
    """Get a specific scam template by ID"""
    return SCAM_TEMPLATES.get(template_id)


def get_all_templates():
    """Get all available scam templates"""
    return SCAM_TEMPLATES
