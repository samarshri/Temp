"""
Vote model - handles upvotes and downvotes
Uses raw MySQL queries
"""

from db import fetch_one, insert, delete as db_delete, update


class Vote:
    """Vote model for post and comment voting"""
    
    def __init__(self, id=None, user_id=None, post_id=None, comment_id=None,
                 vote_type=None, timestamp=None):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.comment_id = comment_id
        self.vote_type = vote_type
        self.timestamp = timestamp
    
    @staticmethod
    def from_dict(data):
        """Create Vote object from database row dict"""
        if not data:
            return None
        return Vote(**data)
    
    @staticmethod
    def get_user_vote_on_post(user_id, post_id):
        """Check if user has voted on a post"""
        query = "SELECT * FROM votes WHERE user_id = %s AND post_id = %s"
        data = fetch_one(query, (user_id, post_id))
        return Vote.from_dict(data)
    
    @staticmethod
    def create_or_update(user_id, post_id=None, comment_id=None, vote_type=1):
        """Create or update a vote"""
        # Check for existing vote
        if post_id:
            existing = Vote.get_user_vote_on_post(user_id, post_id)
            if existing:
                if existing.vote_type == vote_type:
                    # Remove vote (toggle off)
                    return Vote.remove_vote(user_id, post_id=post_id)
                else:
                    # Update vote
                    query = "UPDATE votes SET vote_type = %s WHERE id = %s"
                    update(query, (vote_type, existing.id))
                    return vote_type
        
        # Create new vote
        query = """
        INSERT INTO votes (user_id, post_id, comment_id, vote_type)
        VALUES (%s, %s, %s, %s)
        """
        insert(query, (user_id, post_id, comment_id, vote_type))
        return vote_type
    
    @staticmethod
    def remove_vote(user_id, post_id=None, comment_id=None):
        """Remove a vote"""
        if post_id:
            query = "DELETE FROM votes WHERE user_id = %s AND post_id = %s"
            db_delete(query, (user_id, post_id))
        elif comment_id:
            query = "DELETE FROM votes WHERE user_id = %s AND comment_id = %s"
            db_delete(query, (user_id, comment_id))
        return None
