"""Comment API routes - RESTful endpoints for comments"""
from flask import Blueprint, request, jsonify
from models.post import Post
from models.comment import Comment
from auth_middleware import token_required

comments_bp = Blueprint('comments', __name__, url_prefix='/api')


@comments_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@token_required
def add_comment(current_user, post_id):
    """Add a comment to a post"""
    post = Post.get_by_id(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    data = request.get_json()
    content = data.get('content', '').strip()
    parent_id = data.get('parent_id')
    
    if not content:
        return jsonify({'error': 'Comment content required'}), 400
    
    # Verify parent comment if provided
    if parent_id:
        parent_comment = Comment.get_by_id(parent_id)
        if not parent_comment or parent_comment.post_id != post_id:
            return jsonify({'error': 'Invalid parent comment'}), 400
    
    try:
        comment = Comment.create(post_id, current_user.id, content, parent_id)
        return jsonify({
            'message': 'Comment added successfully',
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'timestamp': comment.timestamp.isoformat() if comment.timestamp else None,
                'author': {
                    'id': current_user.id,
                    'name': current_user.name,
                    'username': current_user.username
                }
            }
        }), 201
    except Exception as e:
        return jsonify({'error': 'Failed to add comment'}), 500


@comments_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@token_required
def update_comment(current_user, comment_id):
    """Update a comment"""
    comment = Comment.get_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'error': 'Comment content required'}), 400
    
    try:
        comment.update_content(content)
        return jsonify({'message': 'Comment updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Update failed'}), 500


@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@token_required
def delete_comment(current_user, comment_id):
    """Delete a comment"""
    comment = Comment.get_by_id(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    if comment.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        comment.delete()
        return jsonify({'message': 'Comment deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Delete failed'}), 500
