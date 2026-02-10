"""
Messages API routes - Direct messaging system
"""

from flask import Blueprint, request, jsonify
from auth_middleware import require_auth
from models.conversation import Conversation
from models.message import Message

messages_bp = Blueprint('messages', __name__, url_prefix='/api')


@messages_bp.route('/conversations', methods=['GET'])
@require_auth
def get_conversations():
    """Get all conversations for current user"""
    try:
        user_id = request.user_id
        conversations = Conversation.get_user_conversations(user_id)
        
        result = []
        for conv in conversations:
            participants = conv.get_participants()
            other_user = next((p for p in participants if p.id != user_id), None)
            
            conv_data = {
                'id': conv.id,
                'type': conv.type,
                'name': conv.name,
                'other_user': {
                    'id': other_user.id,
                    'username': other_user.username,
                    'name': other_user.name,
                    'avatar_url': other_user.avatar_url
                } if other_user else None,
                'unread_count': conv.get_unread_count(user_id),
                'updated_at': conv.updated_at.isoformat() if conv.updated_at else None
            }
            result.append(conv_data)
        
        return jsonify({'conversations': result}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/conversations/<int:conv_id>', methods=['GET'])
@require_auth
def get_conversation(conv_id):
    """Get conversation messages"""
    try:
        user_id = request.user_id
        conv = Conversation.get_by_id(conv_id)
        
        if not conv:
            return jsonify({'error': 'Conversation not found'}), 404
        
        # Mark as read
        conv.mark_as_read(user_id)
        
        # Get messages
        messages = conv.get_messages(limit=100)
        messages_data = [{
            'id': m.id,
            'content': m.content,
            'sender_id': m.sender_id,
            'sender_username': m.sender.username if m.sender else None,
            'sender_name': m.sender.name if m.sender else None,
            'sender_avatar': m.sender.avatar_url if m.sender else None,
            'created_at': m.created_at.isoformat() if m.created_at else None,
            'edited_at': m.edited_at.isoformat() if m.edited_at else None
        } for m in messages]
        
        return jsonify({
            'conversation': {'id': conv.id},
            'messages': messages_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/conversations/start', methods=['POST'])
@require_auth
def start_conversation():
    """Start a new conversation with a user"""
    try:
        data = request.get_json()
        other_user_id = data.get('user_id')
        user_id = request.user_id
        
        if user_id == other_user_id:
            return jsonify({'error': 'Cannot message yourself'}), 400
        
        # Get or create conversation
        conv = Conversation.get_direct_conversation(user_id, other_user_id)
        
        return jsonify({'conversation_id': conv.id}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/conversations/<int:conv_id>/messages', methods=['POST'])
@require_auth
def send_message(conv_id):
    """Send a message in a conversation"""
    try:
        data = request.get_json()
        content = data.get('content')
        user_id = request.user_id
        
        if not content:
            return jsonify({'error': 'Content required'}), 400
        
        message = Message.send(conv_id, user_id, content)
        
        return jsonify({
            'message': {
                'id': message.id,
                'content': message.content,
                'sender_id': message.sender_id,
                'created_at': message.created_at.isoformat() if message.created_at else None
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/messages/<int:message_id>', methods=['PUT'])
@require_auth
def edit_message(message_id):
    """Edit a message"""
    try:
        data = request.get_json()
        new_content = data.get('content')
        user_id = request.user_id
        
        message = Message.get_by_id(message_id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        if message.sender_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        message.edit(new_content)
        return jsonify({'message': 'Message updated'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/messages/<int:message_id>', methods=['DELETE'])
@require_auth
def delete_message(message_id):
    """Delete a message"""
    try:
        user_id = request.user_id
        message = Message.get_by_id(message_id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        if message.sender_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        message.delete()
        return jsonify({'message': 'Message deleted'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/messages/unread-count', methods=['GET'])
@require_auth
def get_unread_count():
    """Get total unread message count"""
    try:
        user_id = request.user_id
        conversations = Conversation.get_user_conversations(user_id)
        
        total_unread = sum(conv.get_unread_count(user_id) for conv in conversations)
        
        return jsonify({'unread_count': total_unread}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
