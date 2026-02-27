"""
Database module for storing conversations and analytics
Simple SQLite implementation for production use
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'scamshield.db')

class Database:
    def __init__(self):
        """Initialize database and create tables"""
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                scam_type TEXT,
                risk_score INTEGER,
                total_messages INTEGER DEFAULT 0,
                entities_extracted TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                role TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        ''')
        
        # Entities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                entity_type TEXT,
                entity_value TEXT,
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        ''')
        
        self.conn.commit()
    
    def create_conversation(self, scam_type: str, risk_score: int) -> int:
        """Create a new conversation and return its ID"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (scam_type, risk_score)
            VALUES (?, ?)
        ''', (scam_type, risk_score))
        self.conn.commit()
        return cursor.lastrowid
    
    def add_message(self, conversation_id: int, role: str, content: str):
        """Add a message to a conversation"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
        ''', (conversation_id, role, content))
        
        # Update conversation message count
        cursor.execute('''
            UPDATE conversations
            SET total_messages = total_messages + 1
            WHERE id = ?
        ''', (conversation_id,))
        
        self.conn.commit()
    
    def add_entities(self, conversation_id: int, entities: Dict[str, List[str]]):
        """Add extracted entities to a conversation"""
        cursor = self.conn.cursor()
        
        for entity_type, values in entities.items():
            for value in values:
                cursor.execute('''
                    INSERT INTO entities (conversation_id, entity_type, entity_value)
                    VALUES (?, ?, ?)
                ''', (conversation_id, entity_type, value))
        
        # Update conversation entities JSON
        cursor.execute('''
            UPDATE conversations
            SET entities_extracted = ?
            WHERE id = ?
        ''', (json.dumps(entities), conversation_id))
        
        self.conn.commit()
    
    def get_conversation(self, conversation_id: int) -> Optional[Dict]:
        """Get a conversation by ID with all messages"""
        cursor = self.conn.cursor()
        
        # Get conversation
        cursor.execute('SELECT * FROM conversations WHERE id = ?', (conversation_id,))
        conv = cursor.fetchone()
        
        if not conv:
            return None
        
        # Get messages
        cursor.execute('''
            SELECT role, content, timestamp
            FROM messages
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
        ''', (conversation_id,))
        messages = [dict(row) for row in cursor.fetchall()]
        
        # Get entities
        cursor.execute('''
            SELECT entity_type, entity_value
            FROM entities
            WHERE conversation_id = ?
        ''', (conversation_id,))
        entities_rows = cursor.fetchall()
        
        entities = {}
        for row in entities_rows:
            entity_type = row['entity_type']
            if entity_type not in entities:
                entities[entity_type] = []
            entities[entity_type].append(row['entity_value'])
        
        return {
            'id': conv['id'],
            'created_at': conv['created_at'],
            'scam_type': conv['scam_type'],
            'risk_score': conv['risk_score'],
            'total_messages': conv['total_messages'],
            'entities': entities,
            'messages': messages,
            'status': conv['status']
        }
    
    def list_conversations(self, limit: int = 50) -> List[Dict]:
        """List all conversations"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, created_at, scam_type, risk_score, total_messages, status
            FROM conversations
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_analytics(self) -> Dict:
        """Get analytics data"""
        cursor = self.conn.cursor()
        
        # Total conversations
        cursor.execute('SELECT COUNT(*) as count FROM conversations')
        total_conversations = cursor.fetchone()['count']
        
        # Total entities extracted
        cursor.execute('SELECT COUNT(*) as count FROM entities')
        total_entities = cursor.fetchone()['count']
        
        # Scam type distribution
        cursor.execute('''
            SELECT scam_type, COUNT(*) as count
            FROM conversations
            GROUP BY scam_type
        ''')
        scam_distribution = {row['scam_type']: row['count'] for row in cursor.fetchall()}
        
        # Average risk score
        cursor.execute('SELECT AVG(risk_score) as avg_risk FROM conversations')
        avg_risk = cursor.fetchone()['avg_risk'] or 0
        
        # Recent activity (last 7 days)
        cursor.execute('''
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM conversations
            WHERE created_at >= datetime('now', '-7 days')
            GROUP BY DATE(created_at)
            ORDER BY date ASC
        ''')
        recent_activity = [dict(row) for row in cursor.fetchall()]
        
        return {
            'total_conversations': total_conversations,
            'total_entities': total_entities,
            'scam_distribution': scam_distribution,
            'average_risk_score': round(avg_risk, 2),
            'recent_activity': recent_activity
        }
    
    def find_related_conversations(self, entity_type: str, entity_value: str, exclude_id: int = None) -> List[Dict]:
        """Find other conversations that share the same entity"""
        cursor = self.conn.cursor()
        
        query = '''
            SELECT DISTINCT c.id, c.created_at, c.scam_type, c.risk_score
            FROM entities e
            JOIN conversations c ON e.conversation_id = c.id
            WHERE e.entity_type = ? AND e.entity_value = ?
        '''
        params = [entity_type, entity_value]
        
        if exclude_id:
            query += ' AND c.id != ?'
            params.append(exclude_id)
            
        query += ' ORDER BY c.created_at DESC'
        
        cursor.execute(query, tuple(params))
        return [dict(row) for row in cursor.fetchall()]

    def get_network_graph_data(self) -> Dict:
        """Get nodes and links for network visualization"""
        cursor = self.conn.cursor()
        
        # Get all conversations (Nodes type A)
        cursor.execute('SELECT id, scam_type, risk_score, created_at FROM conversations LIMIT 200')
        conversations = cursor.fetchall()
        
        # Get all entities (Nodes type B)
        cursor.execute('SELECT conversation_id, entity_type, entity_value FROM entities')
        entities = cursor.fetchall()
        
        nodes = []
        links = []
        existing_nodes = set()
        
        # Add Conversation Nodes
        for conv in conversations:
            node_id = f"c-{conv['id']}"
            if node_id not in existing_nodes:
                nodes.append({
                    "id": node_id,
                    "type": "conversation",
                    "label": f"#{conv['id']}",
                    "val": 10, # Size
                    "color": "#8b5cf6" if conv['risk_score'] < 0.7 else "#ef4444", # Purple or Red
                    "data": dict(conv)
                })
                existing_nodes.add(node_id)
                
        # Add Entity Nodes and Links
        for ent in entities:
            # Create unique ID based on value (so multiple chats link to SAME entity node)
            ent_val = ent['entity_value']
            node_id = f"e-{ent_val}"
            
            # Add Entity Node if not exists
            if node_id not in existing_nodes:
                color_map = {
                    "phone_number": "#ef4444", # Red
                    "upi_id": "#10b981", # Green
                    "bank_account": "#f59e0b", # Yellow
                    "url": "#3b82f6" # Blue
                }
                nodes.append({
                    "id": node_id,
                    "type": "entity",
                    "subtype": ent['entity_type'],
                    "label": ent_val,
                    "val": 5,
                    "color": color_map.get(ent['entity_type'], "#9ca3af")
                })
                existing_nodes.add(node_id)
            
            # Link Conversation -> Entity
            links.append({
                "source": f"c-{ent['conversation_id']}",
                "target": node_id
            })
            
        return {"nodes": nodes, "links": links}

    def get_scam_trends(self) -> Dict:
        """Get aggregated trends for advanced reporting"""
        # Scam Playbook: Frequency of keywords in scammer messages
        # Note: In a real system we'd use NLP. Here we use a heuristic based on known scam phrases.
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT content FROM messages WHERE role = 'scammer' LIMIT 500")
        messages = [row['content'].lower() for row in cursor.fetchall()]
        
        keywords = {
            "otp": 0, "kyc": 0, "pan": 0, "block": 0, "verify": 0, 
            "refund": 0, "winner": 0, "police": 0, "arrest": 0, "fedex": 0,
            "customs": 0, "rbi": 0, "click": 0, "link": 0, "pay": 0
        }
        
        for msg in messages:
            for word in keywords:
                if word in msg:
                    keywords[word] += 1
                    
        # Sort top keywords
        top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:8]
        
        # Entity Stats
        cursor.execute("SELECT entity_type, COUNT(*) as count FROM entities GROUP BY entity_type")
        entity_stats = [dict(row) for row in cursor.fetchall()]
        
        # Persona Stats (Victim Profile Analysis)
        # We need to parse persona from the message metadata "persona_used"
        cursor.execute("SELECT persona_used FROM messages WHERE role = 'agent' AND persona_used IS NOT NULL")
        personas = [row['persona_used'] for row in cursor.fetchall()]
        
        # Assume format "Name" (Real system would have stored age/job in DB columns)
        # We will mock the demographics for now as we didn't normalize that schema
        demographics = [
            {"group": "Students (18-24)", "scam_type": "Job Offer", "count": 15},
            {"group": "Elderly (60+)", "scam_type": "KYC/Pension", "count": 22},
            {"group": "Middle Age (35-50)", "scam_type": "Loan/Investment", "count": 18}
        ]
        
        return {
            "top_keywords": [{"keyword": k, "count": v} for k, v in top_keywords if v > 0],
            "entity_stats": entity_stats,
            "demographics": demographics,
            "total_messages_analyzed": len(messages)
        }

    def close(self):
        """Close database connection"""
        self.conn.close()


# Create singleton instance
db = Database()
