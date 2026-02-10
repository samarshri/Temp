"""
Profiles API routes - User profiles, follow/unfollow
"""

from flask import Blueprint, request, jsonify
from auth_middleware import require_auth
from models.user import User
from db import fetch_one, insert, delete as db_delete

profiles_bp = Blueprint('profiles', __name__, url_prefix='/api')


@profiles_bp.route('/users/<username>', methods=['GET'])
def get_user_profile(username):
    """Get user profile by username"""
    try:
        query = "SELECT * FROM users WHERE username = %s"
        user_data = fetch_one(query, (username,))
        
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        user = User.from_dict(user_data)
        
        # Get follower/following counts
        followers_query = "SELECT COUNT(*) as count FROM user_follows WHERE following_id = %s"
        following_query = "SELECT COUNT(*) as count FROM user_follows WHERE follower_id = %s"
        
        followers_count = fetch_one(followers_query, (user.id,))['count']
        following_count = fetch_one(following_query, (user.id,))['count']
        
        profile_data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'display_name': user.display_name,
            'avatar_url': user.avatar_url,
            'bio': user.bio,
            'status': user.status,
            'branch': user.branch,
            'year': user.year,
            'section': user.section,
            'skills': user.skills,
            'linkedin_url': user.linkedin_url,
            'github_url': user.github_url,
            'reputation_points': user.reputation_points,
            'followers_count': followers_count,
            'following_count': following_count,
            'posts_count': user.get_posts_count(),
            'created_at': user.created_at.isoformat() if user.created_at else None


        }
        
        return jsonify({'user': profile_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profiles_bp.route('/users/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Update current user's profile"""
    try:
        data = request.get_json()
        user_id = request.user_id
        
        from db import update
        query = """
        UPDATE users 
        SET display_name = %s, bio = %s, status = %s, branch = %s, year = %s, 
            section = %s, skills = %s, linkedin_url = %s, github_url = %s, avatar_url = %s
        WHERE id = %s
        """
        
        update(query, (
            data.get('display_name'),
            data.get('bio'),
            data.get('status'),
            data.get('branch'),
            data.get('year'),
            data.get('section'),
            data.get('skills'),
            data.get('linkedin_url'),
            data.get('github_url'),
            data.get('avatar_url'),
            user_id
        ))
        
        return jsonify({'message': 'Profile updated'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profiles_bp.route('/users/<username>/follow', methods=['POST'])
@require_auth
def follow_user(username):
    """Follow a user"""
    try:
        user_id = request.user_id
        
        # Get target user
        query = "SELECT id FROM users WHERE username = %s"
        target_user = fetch_one(query, (username,))
        
        if not target_user:
            return jsonify({'error': 'User not found'}), 404
        
        target_id = target_user['id']
        
        if user_id == target_id:
            return jsonify({'error': 'Cannot follow yourself'}), 400
        
        # Insert follow
        follow_query = """
        INSERT IGNORE INTO user_follows (follower_id, following_id)
        VALUES (%s, %s)
        """
        insert(follow_query, (user_id, target_id))
        
        return jsonify({'message': 'Followed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profiles_bp.route('/users/<username>/follow', methods=['DELETE'])
@require_auth
def unfollow_user(username):
    """Unfollow a user"""
    try:
        user_id = request.user_id
        
        # Get target user
        query = "SELECT id FROM users WHERE username = %s"
        target_user = fetch_one(query, (username,))
        
        if not target_user:
            return jsonify({'error': 'User not found'}), 404
        
        target_id = target_user['id']
        
        # Delete follow
        unfollow_query = """
        DELETE FROM user_follows
        WHERE follower_id = %s AND following_id = %s
        """
        db_delete(unfollow_query, (user_id, target_id))
        
        return jsonify({'message': 'Unfollowed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profiles_bp.route('/users/<username>/followers', methods=['GET'])
def get_followers(username):
    """Get user's followers"""
    try:
        from db import fetch_all
        
        query = """
        SELECT u.id, u.username, u.name, u.avatar_url
        FROM users u
        INNER JOIN user_follows uf ON u.id = uf.follower_id
        INNER JOIN users target ON target.id = uf.following_id
        WHERE target.username = %s
        """
        
        followers = fetch_all(query, (username,))
        return jsonify({'followers': followers or []}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profiles_bp.route('/users/<username>/following', methods=['GET'])
def get_following(username):
    """Get users that this user follows"""
    try:
        from db import fetch_all
        
        query = """
        SELECT u.id, u.username, u.name, u.avatar_url
        FROM users u
        INNER JOIN user_follows uf ON u.id = uf.following_id
        INNER JOIN users target ON target.id = uf.follower_id
        WHERE target.username = %s
        """
        
        following = fetch_all(query, (username,))
        return jsonify({'following': following or []}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@profiles_bp.route('/users/<username>/is-following', methods=['GET'])
@require_auth
def check_following(username):
    """Check if current user follows this user"""
    try:
        user_id = request.user_id
        
        query = """
        SELECT COUNT(*) as count FROM user_follows uf
        INNER JOIN users u ON u.id = uf.following_id
        WHERE uf.follower_id = %s AND u.username = %s
        """
        
        result = fetch_one(query, (user_id, username))
        is_following = result['count'] > 0
        
        return jsonify({'is_following': is_following}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
