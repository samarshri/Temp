"""Post routes - discussion CRUD operations"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import db, Post, Comment
from datetime import datetime
from sqlalchemy import or_, desc

posts_bp = Blueprint('posts', __name__)

# Subject choices for discussions
SUBJECTS = ['Mathematics', 'Science', 'History', 'Literature', 'Computer Science', 
            'Physics', 'Chemistry', 'Biology', 'English', 'Other']


@posts_bp.route('/')
def index():
    """View all discussions with search and filtering"""
    # Get query parameters
    search_query = request.args.get('search', '').strip()
    subject_filter = request.args.get('subject', '')
    sort_by = request.args.get('sort', 'latest')  # latest or most_active
    
    # Base query
    query = Post.query
    
    # Apply search filter
    if search_query:
        query = query.filter(
            or_(
                Post.title.ilike(f'%{search_query}%'),
                Post.content.ilike(f'%{search_query}%')
            )
        )
    
    # Apply subject filter
    if subject_filter and subject_filter in SUBJECTS:
        query = query.filter_by(subject=subject_filter)
    
    # Apply sorting
    if sort_by == 'most_active':
        # Sort by comment count (using subquery)
        query = query.outerjoin(Comment).group_by(Post.id).order_by(desc(db.func.count(Comment.id)))
    else:  # latest
        query = query.order_by(Post.timestamp.desc())
    
    posts = query.all()
    
    return render_template('index.html', 
                         posts=posts, 
                         subjects=SUBJECTS,
                         search_query=search_query,
                         subject_filter=subject_filter,
                         sort_by=sort_by)


@posts_bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new discussion post"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        subject = request.form.get('subject', '')
        
        # Validation
        if not title or not content or not subject:
            flash('Title, content, and subject are required.', 'danger')
            return render_template('create_post.html', subjects=SUBJECTS)
        
        if subject not in SUBJECTS:
            flash('Invalid subject selection.', 'danger')
            return render_template('create_post.html', subjects=SUBJECTS)
        
        # Create post
        post = Post(
            title=title,
            content=content,
            subject=subject,
            user_id=current_user.id
        )
        
        try:
            db.session.add(post)
            db.session.commit()
            flash('Discussion created successfully!', 'success')
            return redirect(url_for('posts.view_post', post_id=post.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            return render_template('create_post.html', subjects=SUBJECTS)
    
    return render_template('create_post.html', subjects=SUBJECTS)


@posts_bp.route('/post/<int:post_id>')
def view_post(post_id):
    """View a single post with comments"""
    post = Post.query.get_or_404(post_id)
    
    # Increment view count
    post.view_count += 1
    db.session.commit()
    
    # Get all comments for this post
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.asc()).all()
    
    return render_template('post.html', post=post, comments=comments)


@posts_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit a post (owner only)"""
    post = Post.query.get_or_404(post_id)
    
    # Check ownership
    if post.user_id != current_user.id:
        flash('You can only edit your own posts.', 'danger')
        return redirect(url_for('posts.view_post', post_id=post_id))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        subject = request.form.get('subject', '')
        
        if not title or not content or not subject:
            flash('All fields are required.', 'danger')
            return render_template('edit_post.html', post=post, subjects=SUBJECTS)
        
        post.title = title
        post.content = content
        post.subject = subject
        post.edited_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('posts.view_post', post_id=post_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    
    return render_template('edit_post.html', post=post, subjects=SUBJECTS)


@posts_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a post (owner or admin)"""
    post = Post.query.get_or_404(post_id)
    
    # Check permissions
    if post.user_id != current_user.id and current_user.role != 'admin':
        flash('You do not have permission to delete this post.', 'danger')
        return redirect(url_for('posts.view_post', post_id=post_id))
    
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully.', 'success')
        return redirect(url_for('posts.index'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
        return redirect(url_for('posts.view_post', post_id=post_id))
