"""
User model - handles user authentication and profile management
Uses raw MySQL queries
"""

from werkzeug.security import generate_password_hash, check_password_hash
from db import fetch_one, fetch_all, insert, update
from datetime import datetime


class User:
    """User model for authentication and profiles"""
    
    def __init__(self, id=None, username=None, name=None, email=None, password_hash=None,
                 role='student', created_at=None, display_name=None, avatar_url=None,
                 bio=None, status=None, branch=None, year=None, section=None, skills=None,
                 linkedin_url=None, github_url=None, reputation_points=0, is_moderator=False,
                 last_seen=None, **kwargs):
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at
        self.display_name = display_name
        self.avatar_url = avatar_url
        self.bio = bio
        self.status = status
        self.branch = branch
        self.year = year
        self.section = section
        self.skills = skills
        self.linkedin_url = linkedin_url
        self.github_url = github_url
        self.reputation_points = reputation_points
        self.is_moderator = is_moderator
        self.last_seen = last_seen
        
        # Store other fields
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    # Flask-Login required properties
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @is_active.setter
    def is_active(self, value):
        # We don't actually store this in this simple model, but we need the setter
        # so that setattr(self, 'is_active', value) doesn't crash
        pass
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def from_dict(data):
        """Create User object from database row dict"""
        if not data:
            return None
        return User(**data)
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = %s"
        data = fetch_one(query, (user_id,))
        return User.from_dict(data)
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        data = fetch_one(query, (email,))
        return User.from_dict(data)
    
    @staticmethod
    def create(username, name, email, password, branch=None, year=None, section=None, role='student'):
        """Create a new user"""
        password_hash = generate_password_hash(password)
        query = """
        INSERT INTO users (username, name, email, password_hash, role, branch, year, section)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        user_id = insert(query, (username, name, email, password_hash, role, branch, year, section))
        return User.get_by_id(user_id)
    
    def update_profile(self, name=None, branch=None, year=None, bio=None,
                      linkedin_url=None, github_url=None):
        """Update user profile"""
        query = """
        UPDATE users 
        SET name = %s, branch = %s, year = %s, bio = %s,
            linkedin_url = %s, github_url = %s
        WHERE id = %s
        """
        update(query, (name, branch, year, bio, linkedin_url, github_url, self.id))
        
        # Update object attributes
        self.name = name
        self.branch = branch
        self.year = year
        self.bio = bio
        self.linkedin_url = linkedin_url
        self.github_url = github_url
    
    def get_posts_count(self):
        """Get number of posts by this user"""
        query = "SELECT COUNT(*) as count FROM posts WHERE user_id = %s"
        result = fetch_one(query, (self.id,))
        return result['count'] if result else 0
    
    def get_comments_count(self):
        """Get number of comments by this user"""
        query = "SELECT COUNT(*) as count FROM comments WHERE user_id = %s"
        result = fetch_one(query, (self.id,))
        return result['count'] if result else 0
    
    def get_recent_posts(self, limit=10):
        """Get user's recent posts"""
        query = """
        SELECT * FROM posts 
        WHERE user_id = %s 
        ORDER BY timestamp DESC 
        LIMIT %s
        """
        from models.post import Post
        posts_data = fetch_all(query, (self.id, limit))
        return [Post.from_dict(p) for p in posts_data] if posts_data else []
