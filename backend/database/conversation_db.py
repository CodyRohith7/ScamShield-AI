"""
Conversation History Database - Persistent storage for all conversations
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class ConversationDatabase:
    """SQLite database for conversation history"""
    
    def __init__(self, db_path: str = "data/conversations.db"):
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT UNIQUE NOT NULL,
                scam_type TEXT,
                persona_used TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                turn_count INTEGER DEFAULT 0,
                risk_score REAL DEFAULT 0.0,
                conversation_phase TEXT,
                extracted_entities TEXT,
                messages TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index on conversation_id for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_conversation_id 
            ON conversations(conversation_id)
        """)
        
        # Create index on status for filtering
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status 
            ON conversations(status)
        """)
        
        # Create index on scam_type for analytics
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_scam_type 
            ON conversations(scam_type)
        """)
        
        conn.commit()
        conn.close()
    
    def save_conversation(self, conversation_data: Dict) -> bool:
        """Save or update conversation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            conversation_id = conversation_data.get('conversation_id')
            
            # Check if conversation exists
            cursor.execute(
                "SELECT id FROM conversations WHERE conversation_id = ?",
                (conversation_id,)
            )
            exists = cursor.fetchone()
            
            if exists:
                # Update existing conversation
                cursor.execute("""
                    UPDATE conversations SET
                        scam_type = ?,
                        persona_used = ?,
                        end_time = ?,
                        turn_count = ?,
                        risk_score = ?,
                        conversation_phase = ?,
                        extracted_entities = ?,
                        messages = ?,
                        status = ?,
                        updated_at = ?
                    WHERE conversation_id = ?
                """, (
                    conversation_data.get('scam_type'),
                    conversation_data.get('persona_used'),
                    conversation_data.get('end_time', datetime.now().isoformat()),
                    conversation_data.get('turn_count', 0),
                    conversation_data.get('risk_score', 0.0),
                    conversation_data.get('conversation_phase'),
                    json.dumps(conversation_data.get('extracted_entities', {})),
                    json.dumps(conversation_data.get('messages', [])),
                    conversation_data.get('status', 'active'),
                    datetime.now().isoformat(),
                    conversation_id
                ))
            else:
                # Insert new conversation
                cursor.execute("""
                    INSERT INTO conversations (
                        conversation_id, scam_type, persona_used, start_time,
                        end_time, turn_count, risk_score, conversation_phase,
                        extracted_entities, messages, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    conversation_id,
                    conversation_data.get('scam_type'),
                    conversation_data.get('persona_used'),
                    conversation_data.get('start_time', datetime.now().isoformat()),
                    conversation_data.get('end_time'),
                    conversation_data.get('turn_count', 0),
                    conversation_data.get('risk_score', 0.0),
                    conversation_data.get('conversation_phase'),
                    json.dumps(conversation_data.get('extracted_entities', {})),
                    json.dumps(conversation_data.get('messages', [])),
                    conversation_data.get('status', 'active')
                ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get conversation by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM conversations 
                WHERE conversation_id = ? AND status != 'deleted'
            """, (conversation_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return self._row_to_dict(row)
            return None
            
        except Exception as e:
            print(f"Error getting conversation: {e}")
            return None
    
    def list_conversations(self, limit: int = 100, offset: int = 0, 
                          status: str = None, scam_type: str = None) -> List[Dict]:
        """List conversations with optional filters"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Build query with filters
            query = "SELECT * FROM conversations WHERE status != 'deleted'"
            params = []
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            if scam_type:
                query += " AND scam_type = ?"
                params.append(scam_type)
            
            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            return [self._row_to_dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error listing conversations: {e}")
            return []
    
    def delete_conversation(self, conversation_id: str, hard_delete: bool = False) -> bool:
        """Delete conversation (soft delete by default)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if hard_delete:
                # Permanently delete
                cursor.execute(
                    "DELETE FROM conversations WHERE conversation_id = ?",
                    (conversation_id,)
                )
            else:
                # Soft delete (mark as deleted)
                cursor.execute("""
                    UPDATE conversations 
                    SET status = 'deleted', updated_at = ?
                    WHERE conversation_id = ?
                """, (datetime.now().isoformat(), conversation_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error deleting conversation: {e}")
            return False
    
    def search_conversations(self, query: str, limit: int = 50) -> List[Dict]:
        """Search conversations by content"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Search in messages and extracted entities
            cursor.execute("""
                SELECT * FROM conversations 
                WHERE status != 'deleted' 
                AND (messages LIKE ? OR extracted_entities LIKE ?)
                ORDER BY created_at DESC
                LIMIT ?
            """, (f'%{query}%', f'%{query}%', limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [self._row_to_dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error searching conversations: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total conversations
            cursor.execute("SELECT COUNT(*) FROM conversations WHERE status != 'deleted'")
            total = cursor.fetchone()[0]
            
            # Active conversations
            cursor.execute("SELECT COUNT(*) FROM conversations WHERE status = 'active'")
            active = cursor.fetchone()[0]
            
            # Completed conversations
            cursor.execute("SELECT COUNT(*) FROM conversations WHERE status = 'completed'")
            completed = cursor.fetchone()[0]
            
            # Scam type distribution
            cursor.execute("""
                SELECT scam_type, COUNT(*) as count 
                FROM conversations 
                WHERE status != 'deleted' AND scam_type IS NOT NULL
                GROUP BY scam_type
            """)
            scam_types = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Total entities extracted
            cursor.execute("""
                SELECT extracted_entities 
                FROM conversations 
                WHERE status != 'deleted' AND extracted_entities IS NOT NULL
            """)
            total_entities = 0
            for row in cursor.fetchall():
                try:
                    entities = json.loads(row[0])
                    # Count all entity types
                    for entity_list in entities.values():
                        if isinstance(entity_list, list):
                            total_entities += len(entity_list)
                except:
                    pass
            
            conn.close()
            
            return {
                'total_conversations': total,
                'active_conversations': active,
                'completed_conversations': completed,
                'scam_type_distribution': scam_types,
                'total_entities_extracted': total_entities
            }
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def export_all(self, format: str = 'json') -> str:
        """Export all conversations"""
        try:
            conversations = self.list_conversations(limit=10000)
            
            if format == 'json':
                return json.dumps(conversations, indent=2)
            elif format == 'csv':
                # TODO: Implement CSV export
                pass
            
            return ""
            
        except Exception as e:
            print(f"Error exporting conversations: {e}")
            return ""
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """Convert database row to dictionary"""
        data = dict(row)
        
        # Parse JSON fields
        if data.get('extracted_entities'):
            try:
                data['extracted_entities'] = json.loads(data['extracted_entities'])
            except:
                data['extracted_entities'] = {}
        
        if data.get('messages'):
            try:
                data['messages'] = json.loads(data['messages'])
            except:
                data['messages'] = []
        
        return data
    
    def cleanup_old_conversations(self, days: int = 30) -> int:
        """Delete conversations older than specified days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            cursor.execute("""
                DELETE FROM conversations 
                WHERE status = 'deleted' 
                AND datetime(updated_at) < datetime(?, 'unixepoch')
            """, (cutoff_date,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return deleted_count
            
        except Exception as e:
            print(f"Error cleaning up conversations: {e}")
            return 0


# Global instance
conversation_db = ConversationDatabase()


# Convenience functions
def save_conversation(conversation_data: Dict) -> bool:
    """Save conversation to database"""
    return conversation_db.save_conversation(conversation_data)


def get_conversation(conversation_id: str) -> Optional[Dict]:
    """Get conversation from database"""
    return conversation_db.get_conversation(conversation_id)


def list_conversations(limit: int = 100, **filters) -> List[Dict]:
    """List conversations"""
    return conversation_db.list_conversations(limit=limit, **filters)


def delete_conversation(conversation_id: str, hard_delete: bool = False) -> bool:
    """Delete conversation"""
    return conversation_db.delete_conversation(conversation_id, hard_delete)


def search_conversations(query: str) -> List[Dict]:
    """Search conversations"""
    return conversation_db.search_conversations(query)


def get_statistics() -> Dict:
    """Get conversation statistics"""
    return conversation_db.get_statistics()
