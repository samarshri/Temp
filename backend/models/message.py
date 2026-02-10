"""
Message model - handles direct messages
Uses raw MySQL queries
"""

from db import fetch_one, fetch_all, insert, update, delete as db_delete
from datetime import datetime


class Message:
    """Message model for direct messaging"""
    
    def __init__(self, id=None, conversation_id=None, sender_id=None, content=None,
                 message_type='text', attachment_url=None, is_read=False, is_deleted=False,
                 created_at=None, edited_at=None, sender=None):
        self.id = id
        self.conversation_id = conversation_id
        self.sender_id = sender_id
        self.content = content
        self.message_type = message_type
        self.attachment_url = attachment_url
        self.is_read = is_read
        self.is_deleted = is_deleted
        self.created_at = created_at
        self.edited_at = edited_at
        self._sender = sender
    
    @property
    def sender(self):
        """Lazy load sender"""
        if not self._sender and self.sender_id:
            from models.user import User
            self._sender = User.get_by_id(self.sender_id)
        return self._sender
    
    @staticmethod
    def from_dict(data):
        """Create Message object from database row dict"""
        if not data:
            return None
        return Message(**data)
    
    @staticmethod
    def get_by_id(message_id):
        """Get message by ID"""
        query = "SELECT * FROM messages WHERE id = %s"
        data = fetch_one(query, (message_id,))
        return Message.from_dict(data)
    
    @staticmethod
    def send(conversation_id, sender_id, content, message_type='text', attachment_url=None):
        """Send a new message"""
        query = """
        INSERT INTO messages (conversation_id, sender_id, content, message_type, attachment_url)
        VALUES (%s, %s, %s, %s, %s)
        """
        message_id = insert(query, (conversation_id, sender_id, content, message_type, attachment_url))
        
        # Update conversation timestamp using Python side datetime
        now = datetime.utcnow()
        update_conv = "UPDATE conversations SET updated_at = %s WHERE id = %s"
        update(update_conv, (now, conversation_id))
        
        return Message.get_by_id(message_id)
    
    def edit(self, new_content):
        """Edit message content"""
        now = datetime.utcnow()
        query = """
        UPDATE messages
        SET content = %s, edited_at = %s
        WHERE id = %s
        """
        update(query, (new_content, now, self.id))
        self.content = new_content
        self.edited_at = now
    
    def delete(self):
        """Soft delete message"""
        # Use 1 instead of TRUE for maximum SQLite/MySQL compatibility
        query = "UPDATE messages SET is_deleted = 1 WHERE id = %s"
        update(query, (self.id,))
        self.is_deleted = True
    
    def add_reaction(self, user_id, emoji):
        """Add emoji reaction to message"""
        query = """
        INSERT INTO message_reactions (message_id, user_id, emoji)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE emoji = %s
        """
        insert(query, (self.id, user_id, emoji, emoji))
    
    def get_reactions(self):
        """Get all reactions for this message"""
        query = """
        SELECT emoji, COUNT(*) as count
        FROM message_reactions
        WHERE message_id = %s
        GROUP BY emoji
        """
        return fetch_all(query, (self.id,)) or []
