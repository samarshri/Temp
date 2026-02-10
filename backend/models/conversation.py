"""
Conversation model - handles direct messaging conversations
Uses raw MySQL queries
"""

from db import fetch_one, fetch_all, insert, update, delete as db_delete
from datetime import datetime


class Conversation:
    """Conversation model for direct messages"""
    
    def __init__(self, id=None, type='direct', name=None, created_at=None, updated_at=None, **kwargs):
        self.id = id
        self.type = type
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        
        # Store other fields as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @staticmethod
    def from_dict(data):
        """Create Conversation object from database row dict"""
        if not data:
            return None
        return Conversation(**data)
    
    @staticmethod
    def get_by_id(conversation_id):
        """Get conversation by ID"""
        query = "SELECT * FROM conversations WHERE id = %s"
        data = fetch_one(query, (conversation_id,))
        return Conversation.from_dict(data)
    
    @staticmethod
    def create(type='direct', name=None, user_ids=None):
        """Create a new conversation with participants"""
        query = "INSERT INTO conversations (type, name) VALUES (%s, %s)"
        conv_id = insert(query, (type, name))
        
        # Add participants
        if user_ids:
            for user_id in user_ids:
                Conversation.add_participant(conv_id, user_id)
        
        return Conversation.get_by_id(conv_id)
    
    @staticmethod
    def add_participant(conversation_id, user_id):
        """Add a participant to conversation"""
        query = """
        INSERT INTO conversation_participants (conversation_id, user_id)
        VALUES (%s, %s)
        """
        insert(query, (conversation_id, user_id))
    
    @staticmethod
    def get_user_conversations(user_id):
        """Get all conversations for a user"""
        query = """
        SELECT c.*, MAX(m.created_at) as last_message_at
        FROM conversations c
        INNER JOIN conversation_participants cp ON c.id = cp.conversation_id
        LEFT JOIN messages m ON c.id = m.conversation_id
        WHERE cp.user_id = %s
        GROUP BY c.id
        ORDER BY last_message_at DESC
        """
        convs_data = fetch_all(query, (user_id,))
        return [Conversation.from_dict(c) for c in convs_data] if convs_data else []
    
    @staticmethod
    def get_direct_conversation(user_id1, user_id2):
        """Get direct conversation between two users, create if doesn't exist"""
        query = """
        SELECT c.* FROM conversations c
        INNER JOIN conversation_participants cp1 ON c.id = cp1.conversation_id
        INNER JOIN conversation_participants cp2 ON c.id = cp2.conversation_id
        WHERE c.type = 'direct'
        AND cp1.user_id = %s
        AND cp2.user_id = %s
        """
        data = fetch_one(query, (user_id1, user_id2))
        
        if data:
            return Conversation.from_dict(data)
        else:
            # Create new conversation
            return Conversation.create(type='direct', user_ids=[user_id1, user_id2])
    
    def get_participants(self):
        """Get participants of this conversation"""
        query = """
        SELECT u.* FROM users u
        INNER JOIN conversation_participants cp ON u.id = cp.user_id
        WHERE cp.conversation_id = %s
        """
        from models.user import User
        users_data = fetch_all(query, (self.id,))
        return [User.from_dict(u) for u in users_data] if users_data else []
    
    def get_messages(self, limit=50, offset=0):
        """Get messages in this conversation"""
        query = """
        SELECT * FROM messages
        WHERE conversation_id = %s
        AND is_deleted = FALSE
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
        """
        from models.message import Message
        msgs_data = fetch_all(query, (self.id, limit, offset))
        return [Message.from_dict(m) for m in msgs_data] if msgs_data else []
    
    def get_unread_count(self, user_id):
        """Get unread message count for a user"""
        query = """
        SELECT COUNT(*) as count FROM messages m
        LEFT JOIN conversation_participants cp ON m.conversation_id = cp.conversation_id AND cp.user_id = %s
        WHERE m.conversation_id = %s
        AND m.sender_id != %s
        AND m.created_at > COALESCE(cp.last_read_at, '1970-01-01')
        """
        result = fetch_one(query, (user_id, self.id, user_id))
        return result['count'] if result else 0
    
    def mark_as_read(self, user_id):
        """Mark all messages as read for a user"""
        now = datetime.utcnow()
        query = """
        UPDATE conversation_participants
        SET last_read_at = %s
        WHERE conversation_id = %s AND user_id = %s
        """
        update(query, (now, self.id, user_id))
