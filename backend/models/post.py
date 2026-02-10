"""
Post model - handles discussion posts
Uses raw MySQL queries
"""

from db import fetch_one, fetch_all, insert, update, delete as db_delete
from datetime import datetime


class Post:
    """Post model for discussion threads"""
    
    def __init__(self, id=None, user_id=None, title=None, content=None,
                 subject=None, timestamp=None, edited_at=None, view_count=0,
                 upvotes=0, downvotes=0, author=None, **kwargs):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.subject = subject
        self.timestamp = timestamp
        self.edited_at = edited_at
        self.view_count = view_count
        self.upvotes = upvotes
        self.downvotes = downvotes
        self._author = author
        
        # Store other fields as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @property
    def score(self):
        """Calculate score (upvotes - downvotes)"""
        return self.upvotes - self.downvotes
    
    @property
    def author(self):
        """Lazy load author"""
        if not self._author and self.user_id:
            from models.user import User
            self._author = User.get_by_id(self.user_id)
        return self._author
    
    @staticmethod
    def from_dict(data):
        """Create Post object from database row dict"""
        if not data:
            return None
            
        # Handle SQLite string timestamps
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            try:
                data['timestamp'] = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
        
        edited_at = data.get('edited_at')
        if isinstance(edited_at, str):
            try:
                data['edited_at'] = datetime.strptime(edited_at, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
                
        return Post(**data)
    
    @staticmethod
    def get_all(search=None, subject=None, sort_by='latest', limit=100):
        """Get all posts with optional filters"""
        query = """
        SELECT * FROM posts WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (title LIKE %s OR content LIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        if subject:
            query += " AND subject = %s"
            params.append(subject)
        
        # Sorting
        if sort_by == 'top':
            query += " ORDER BY (upvotes - downvotes) DESC"
        elif sort_by == 'most_active':
            query = """
            SELECT p.*, COUNT(c.id) as comment_count
            FROM posts p
            LEFT JOIN comments c ON p.id = c.post_id
            WHERE 1=1
            """
            if search:
                query += " AND (p.title LIKE %s OR p.content LIKE %s)"
            if subject:
                query += " AND p.subject = %s"
            query += " GROUP BY p.id ORDER BY comment_count DESC"
        else:  # latest
            query += " ORDER BY timestamp DESC"
        
        query += f" LIMIT {limit}"
        
        posts_data = fetch_all(query, tuple(params))
        return [Post.from_dict(p) for p in posts_data] if posts_data else []
    
    @staticmethod
    def get_by_id(post_id):
        """Get post by ID"""
        query = "SELECT * FROM posts WHERE id = %s"
        data = fetch_one(query, (post_id,))
        return Post.from_dict(data)
    
    @staticmethod
    def create(user_id, title, content, subject):
        """Create a new post - compatible with schema_v2"""
        query = """
        INSERT INTO posts (user_id, title, content, subject)
        VALUES (%s, %s, %s, %s)
        """
        # Use subject as category (they're the same in our forum setup)
        post_id = insert(query, (user_id, title, content, subject))
        return Post.get_by_id(post_id)
    
    def update_content(self, title, content, subject):
        """Update post content"""
        query = """
        UPDATE posts 
        SET title = %s, content = %s, subject = %s, edited_at = NOW()
        WHERE id = %s
        """
        update(query, (title, content, subject, self.id))
        self.title = title
        self.content = content
        self.subject = subject
        self.edited_at = datetime.now()
    
    def increment_view_count(self):
        """Increment view count"""
        query = "UPDATE posts SET view_count = view_count + 1 WHERE id = %s"
        update(query, (self.id,))
        self.view_count += 1
    
    def delete(self):
        """Delete post"""
        query = "DELETE FROM posts WHERE id = %s"
        db_delete(query, (self.id,))
    
    def comment_count(self):
        """Get number of comments"""
        query = "SELECT COUNT(*) as count FROM comments WHERE post_id = %s"
        result = fetch_one(query, (self.id,))
        return result['count'] if result else 0
