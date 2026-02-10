"""  
Comment model - handles comment threads and replies
Uses raw MySQL queries
"""

from db import fetch_one, fetch_all, insert, update, delete as db_delete
from datetime import datetime


class Comment:
    """Comment model for threaded discussions"""
    
    def __init__(self, id=None, post_id=None, user_id=None, parent_id=None,
                 content=None, timestamp=None, edited_at=None, author=None, **kwargs):
        self.id = id
        self.post_id = post_id
        self.user_id = user_id
        self.parent_id = parent_id
        self.content = content
        self.timestamp = timestamp
        self.edited_at = edited_at
        self._author = author
        self._replies = None
        
        # Store other fields as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @property
    def author(self):
        """Lazy load author"""
        if not self._author and self.user_id:
            from models.user import User
            self._author = User.get_by_id(self.user_id)
        return self._author
    
    @property
    def replies(self):
        """Lazy load replies"""
        if self._replies is None:
            self._replies = Comment.get_by_parent(self.id)
        return self._replies
    
    @staticmethod
    def from_dict(data):
        """Create Comment object from database row dict"""
        if not data:
            return None
        
        # Handle SQLite string timestamps
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            try:
                data['timestamp'] = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass

        if isinstance(data.get('edited_at'), str):
            try:
                data['edited_at'] = datetime.strptime(data['edited_at'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
                
        return Comment(**data)
    
    @staticmethod
    def get_by_id(comment_id):
        """Get comment by ID"""
        query = "SELECT * FROM comments WHERE id = %s"
        data = fetch_one(query, (comment_id,))
        return Comment.from_dict(data)
    
    @staticmethod
    def get_by_post(post_id, parent_only=False):
        """Get comments for a post"""
        if parent_only:
            query = """
            SELECT * FROM comments 
            WHERE post_id = %s AND parent_id IS NULL
            ORDER BY timestamp ASC
            """
        else:
            query = """
            SELECT * FROM comments 
            WHERE post_id = %s
            ORDER BY timestamp ASC
            """
        comments_data = fetch_all(query, (post_id,))
        return [Comment.from_dict(c) for c in comments_data] if comments_data else []
    
    @staticmethod
    def get_by_parent(parent_id):
        """Get replies to a comment"""
        query = """
        SELECT * FROM comments 
        WHERE parent_id = %s
        ORDER BY timestamp ASC
        """
        comments_data = fetch_all(query, (parent_id,))
        return [Comment.from_dict(c) for c in comments_data] if comments_data else []
    
    @staticmethod
    def create(post_id, user_id, content, parent_id=None):
        """Create a new comment"""
        query = """
        INSERT INTO comments (post_id, user_id, content, parent_id)
        VALUES (%s, %s, %s, %s)
        """
        comment_id = insert(query, (post_id, user_id, content, parent_id))
        return Comment.get_by_id(comment_id)
    
    def update_content(self, content):
        """Update comment content"""
        query = """
        UPDATE comments 
        SET content = %s, edited_at = NOW()
        WHERE id = %s
        """
        update(query, (content, self.id))
        self.content = content
        self.edited_at = datetime.now()
    
    def delete(self):
        """Delete comment"""
        query = "DELETE FROM comments WHERE id = %s"
        db_delete(query, (self.id,))
