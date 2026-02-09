"""Comment routes - add, edit, delete comments"""
from flask import Blueprint, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from models import db, Post, Comment
from datetime import datetime

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """Add a comment to a post"""
    post = Post.query.get_or_404(post_id)
    
    content = request.form.get('content', '').strip()
    
    if not content:
        flash('Comment cannot be empty.', 'danger')
        return redirect(url_for('posts.view_post', post_id=post_id))
    
    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=content
    )
    
    try:
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('posts.view_post', post_id=post_id))


@comments_bp.route('/comment/<int:comment_id>/edit', methods=['POST'])
@login_required
def edit_comment(comment_id):
    """Edit a comment (owner only)"""
    comment = Comment.query.get_or_404(comment_id)
    
    # Check ownership
    if comment.user_id != current_user.id:
        flash('You can only edit your own comments.', 'danger')
        return redirect(url_for('posts.view_post', post_id=comment.post_id))
    
    content = request.form.get('content', '').strip()
    
    if not content:
        flash('Comment cannot be empty.', 'danger')
        return redirect(url_for('posts.view_post', post_id=comment.post_id))
    
    comment.content = content
    comment.edited_at = datetime.utcnow()
    
    try:
        db.session.commit()
        flash('Comment updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('posts.view_post', post_id=comment.post_id))


@comments_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """Delete a comment (owner or admin)"""
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id
    
    # Check permissions
    if comment.user_id != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to delete this comment.', 'danger')
        return redirect(url_for('posts.view_post', post_id=post_id))
    
    try:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
    
    return redirect(url_for('posts.view_post', post_id=post_id))
