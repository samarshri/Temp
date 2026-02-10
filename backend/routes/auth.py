"""Authentication API routes - JWT-based authentication"""
from flask import Blueprint, request, jsonify
from models.user import User
from auth_middleware import generate_token, token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration - returns JWT token"""
    data = request.get_json()
    
    username = data.get('username', '').strip()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    branch = data.get('branch', '').strip()
    year = data.get('year', '').strip()
    section = data.get('section', '').strip()
    
    # Validation
    if not username or not name or not email or not password:
        return jsonify({'error': 'Username, name, email, and password are required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if email exists
    if User.get_by_email(email):
        return jsonify({'error': 'Email already registered'}), 400
    
    # Check if username exists (case-insensitive)
    from db import fetch_one
    check_username = fetch_one("SELECT id FROM users WHERE LOWER(username) = LOWER(%s)", (username,))
    if check_username:
        return jsonify({'error': 'Username already taken'}), 400
    
    # Create user
    try:
        user = User.create(username, name, email, password, branch, year, section)
        token = generate_token(user.id)
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'branch': user.branch,
                'year': user.year,
                'section': user.section,
                'role': user.role
            }
        }), 201
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login - returns JWT token"""
    data = request.get_json()
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.get_by_email(email)
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = generate_token(user.id)
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'branch': user.branch,
            'year': user.year,
            'section': user.section,
            'role': user.role,
            'bio': user.bio,
            'avatar_url': user.avatar_url,
            'linkedin_url': user.linkedin_url,
            'github_url': user.github_url,
            'reputation_points': user.reputation_points
        }
    }), 200


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current authenticated user"""
    return jsonify({
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'name': current_user.name,
            'email': current_user.email,
            'branch': getattr(current_user, 'branch', ''),
            'year': getattr(current_user, 'year', ''),
            'role': current_user.role,
            'bio': getattr(current_user, 'bio', ''),
            'avatar_url': getattr(current_user, 'avatar_url', ''),
            'linkedin_url': getattr(current_user, 'linkedin_url', ''),
            'github_url': getattr(current_user, 'github_url', ''),
            'posts_count': current_user.get_posts_count(),
            'comments_count': current_user.get_comments_count()
        }
    }), 200


@auth_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """Get user profile by ID"""
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    posts = user.get_recent_posts(limit=10)
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'branch': getattr(user, 'branch', ''),
            'year': getattr(user, 'year', ''),
            'bio': getattr(user, 'bio', ''),
            'avatar_url': getattr(user, 'avatar_url', ''),
            'linkedin_url': getattr(user, 'linkedin_url', ''),
            'github_url': getattr(user, 'github_url', ''),
            'posts_count': user.get_posts_count(),
            'comments_count': user.get_comments_count()
        },
        'posts': [{
            'id': p.id,
            'title': p.title,
            'content': p.content[:150],
            'subject': p.subject,
            'timestamp': p.timestamp.isoformat() if p.timestamp else None,
            'score': p.score,
            'comment_count': p.comment_count()
        } for p in posts]
    }), 200


@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update current user's profile"""
    data = request.get_json()
    
    name = data.get('name', '').strip()
    branch = data.get('branch', '').strip()
    year = data.get('year', '').strip()
    bio = data.get('bio', '').strip()
    linkedin_url = data.get('linkedin_url', '').strip()
    github_url = data.get('github_url', '').strip()
    
    try:
        current_user.update_profile(name, branch, year, bio, linkedin_url, github_url)
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Update failed'}), 500
