"""AI feature routes - REST API endpoints for AI functionality"""
from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import Post, Comment
from ai_service import AIService
from config import Config

ai_bp = Blueprint('ai', __name__)

# Initialize AI service
ai_service = AIService(
    provider=Config.AI_PROVIDER,
    api_key=Config.OPENAI_API_KEY,
    model=Config.AI_MODEL
)


@ai_bp.route('/ai/answer', methods=['POST'])
@login_required
def get_ai_answer():
    """Get AI-generated answer for a discussion"""
    data = request.get_json()
    post_id = data.get('post_id')
    
    if not post_id:
        return jsonify({'success': False, 'error': 'Post ID required'}), 400
    
    post = Post.query.get_or_404(post_id)
    
    result = ai_service.get_answer_for_discussion(
        title=post.title,
        content=post.content,
        subject=post.subject
    )
    
    return jsonify(result)


@ai_bp.route('/ai/moderate', methods=['POST'])
@login_required
def moderate_content():
    """Check content for spam/abuse before posting"""
    data = request.get_json()
    content = data.get('content', '')
    
    if not content:
        return jsonify({'success': False, 'error': 'Content required'}), 400
    
    result = ai_service.moderate_content(content)
    
    return jsonify(result)


@ai_bp.route('/ai/summarize', methods=['POST'])
@login_required
def summarize_thread():
    """Generate summary of a discussion thread"""
    data = request.get_json()
    post_id = data.get('post_id')
    
    if not post_id:
        return jsonify({'success': False, 'error': 'Post ID required'}), 400
    
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    comment_texts = [c.content for c in comments]
    
    result = ai_service.summarize_thread(
        title=post.title,
        content=post.content,
        comments=comment_texts
    )
    
    return jsonify(result)


@ai_bp.route('/ai/enhance', methods=['POST'])
@login_required
def enhance_question():
    """Improve a student's question"""
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({'success': False, 'error': 'Question required'}), 400
    
    result = ai_service.enhance_question(question)
    
    return jsonify(result)
