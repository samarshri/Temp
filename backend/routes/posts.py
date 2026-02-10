"""Post API routes - RESTful endpoints for posts"""
from flask import Blueprint, request, jsonify
from models.post import Post
from models.vote import Vote
from auth_middleware import token_required, get_current_user
from db import update as db_update

posts_bp = Blueprint('posts', __name__, url_prefix='/api/posts')

SUBJECTS = ['Coding', 'Studies', 'General Discussion', 'Placement', 'Projects',
            'Resources', 'Internships', 'Hackathons', 'Clubs']


@posts_bp.route('', methods=['GET'])
def get_posts():
    """Get all posts with optional filtering"""
    search = request.args.get('search', '')
    subject = request.args.get('subject', '')
    sort_by = request.args.get('sort', 'latest')
    
    posts = Post.get_all(
        search=search if search else None,
        subject=subject if subject in SUBJECTS else None,
        sort_by=sort_by
    )
    
    return jsonify({
        'posts': [{
            'id': p.id,
            'title': p.title,
            'content': p.content,
            'subject': p.subject,
            'timestamp': p.timestamp.isoformat() if p.timestamp else None,
            'edited_at': p.edited_at.isoformat() if getattr(p, 'edited_at', None) else None,
            'view_count': getattr(p, 'view_count', 0),
            'upvotes': getattr(p, 'upvotes', 0),
            'downvotes': getattr(p, 'downvotes', 0),
            'score': p.score,
            'author': {
                'id': p.author.id,
                'username': p.author.username,
                'name': p.author.name,
                'branch': getattr(p.author, 'branch', ''),
                'year': getattr(p.author, 'year', '')
            } if p.author else None,
            'comment_count': p.comment_count()
        } for p in posts],
        'subjects': SUBJECTS
    }), 200


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get single post by ID"""
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    # Increment view count
    try:
        post.increment_view_count()
        
        # Get comments
        from models.comment import Comment
        comments = Comment.get_by_post(post_id, parent_only=True)
        
        def serialize_comment(c):
            return {
                'id': c.id,
                'content': c.content,
                'timestamp': c.timestamp.isoformat() if c.timestamp else None,
                'edited_at': c.edited_at.isoformat() if c.edited_at else None,
                'author': {
                    'id': c.author.id,
                    'name': c.author.name,
                    'avatar_url': getattr(c.author, 'avatar_url', '')
                } if c.author else None,
                'replies': [serialize_comment(r) for r in c.replies]
            }
        
        return jsonify({
            'post': {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'subject': post.subject,
                'timestamp': post.timestamp.isoformat() if post.timestamp else None,
                'edited_at': post.edited_at.isoformat() if getattr(post, 'edited_at', None) else None,
                'view_count': getattr(post, 'view_count', 0),
                'upvotes': getattr(post, 'upvotes', 0),
                'downvotes': getattr(post, 'downvotes', 0),
                'score': post.score,
                'author': {
                    'id': post.author.id,
                    'username': post.author.username,
                    'name': post.author.name,
                    'branch': getattr(post.author, 'branch', ''),
                    'year': getattr(post.author, 'year', ''),
                    'avatar_url': getattr(post.author, 'avatar_url', '')
                } if post.author else None,
                'user_id': post.user_id
            },
            'comments': [serialize_comment(c) for c in comments]
        }), 200
    except Exception as e:
        print(f"Error fetching post: {str(e)}")
        return jsonify({'error': 'Failed to fetch post'}), 500


@posts_bp.route('', methods=['POST'])
@token_required
def create_post(current_user):
    """Create a new post"""
    data = request.get_json()
    
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    subject = data.get('subject', '')
    
    if not title or not content or not subject:
        return jsonify({'error': 'Title, content, and subject are required'}), 400
    
    if subject not in SUBJECTS:
        return jsonify({'error': 'Invalid subject'}), 400
    
    try:
        post = Post.create(current_user.id, title, content, subject)
        return jsonify({
            'message': 'Post created successfully',
            'post': {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'subject': post.subject
            }
        }), 201
    except Exception as e:
        print(f"Error creating post: {str(e)}")
        return jsonify({'error': 'Failed to create post'}), 500


@posts_bp.route('/<int:post_id>', methods=['PUT'])
@token_required
def update_post(current_user, post_id):
    """Update a post"""
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    if post.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    subject = data.get('subject', '')
    
    if not title or not content or not subject:
        return jsonify({'error': 'All fields required'}), 400
    
    try:
        post.update_content(title, content, subject)
        return jsonify({'message': 'Post updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Update failed'}), 500


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user, post_id):
    """Delete a post"""
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    if post.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        post.delete()
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Delete failed'}), 500


@posts_bp.route('/<int:post_id>/vote', methods=['POST'])
@token_required
def vote_on_post(current_user, post_id):
    """Vote on a post"""
    data = request.get_json()
    vote_type = data.get('vote_type')
    
    if vote_type not in [1, -1]:
        return jsonify({'error': 'Invalid vote type'}), 400
    
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    try:
        existing_vote = Vote.get_user_vote_on_post(current_user.id, post_id)
        
        if existing_vote:
            if existing_vote.vote_type == vote_type:
                # Remove vote (toggle)
                Vote.remove_vote(current_user.id, post_id=post_id)
                if vote_type == 1:
                    db_update("UPDATE posts SET upvotes = upvotes - 1 WHERE id = %s", (post_id,))
                    post.upvotes -= 1
                else:
                    db_update("UPDATE posts SET downvotes = downvotes - 1 WHERE id = %s", (post_id,))
                    post.downvotes -= 1
            else:
                # Change vote
                Vote.create_or_update(current_user.id, post_id=post_id, vote_type=vote_type)
                if existing_vote.vote_type == 1:
                    db_update("UPDATE posts SET upvotes = upvotes - 1, downvotes = downvotes + 1 WHERE id = %s", (post_id,))
                    post.upvotes -= 1
                    post.downvotes += 1
                else:
                    db_update("UPDATE posts SET downvotes = downvotes - 1, upvotes = upvotes + 1 WHERE id = %s", (post_id,))
                    post.downvotes -= 1
                    post.upvotes += 1
        else:
            # New vote
            Vote.create_or_update(current_user.id, post_id=post_id, vote_type=vote_type)
            if vote_type == 1:
                db_update("UPDATE posts SET upvotes = upvotes + 1 WHERE id = %s", (post_id,))
                post.upvotes += 1
            else:
                db_update("UPDATE posts SET downvotes = downvotes + 1 WHERE id = %s", (post_id,))
                post.downvotes += 1
        
        return jsonify({
            'upvotes': post.upvotes,
            'downvotes': post.downvotes,
            'score': post.score
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
