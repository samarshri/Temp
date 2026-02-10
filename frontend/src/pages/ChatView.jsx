import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { messagesAPI } from '../utils/api';
import { useAuth } from '../context/AuthContext';

const ChatView = () => {
    const { conversationId } = useParams();
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const [sending, setSending] = useState(false);
    const { user } = useAuth();
    const navigate = useNavigate();
    const messagesEndRef = useRef(null);

    useEffect(() => {
        if (conversationId) {
            fetchMessages();
            const interval = setInterval(fetchMessages, 3000); // Poll every 3 seconds
            return () => clearInterval(interval);
        }
    }, [conversationId]);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const fetchMessages = async () => {
        try {
            const response = await messagesAPI.getConversation(conversationId);
            setMessages(response.data.messages.reverse());
            setLoading(false);
        } catch (error) {
            console.error('Error fetching messages:', error);
            setLoading(false);
        }
    };

    const handleSend = async (e) => {
        e.preventDefault();
        if (!newMessage.trim()) return;

        setSending(true);
        try {
            await messagesAPI.sendMessage(conversationId, newMessage);
            setNewMessage('');
            await fetchMessages();
        } catch (error) {
            console.error('Error sending message:', error);
        }
        setSending(false);
    };

    const formatTime = (timestamp) => {
        if (!timestamp) return '';
        const date = new Date(timestamp);
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    };

    if (loading) {
        return (
            <div className="container mt-4 text-center">
                <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    return (
        <div className="container-fluid mt-3" style={{ height: 'calc(100vh - 100px)' }}>
            <div className="row h-100">
                <div className="col-lg-8 mx-auto h-100">
                    <div className="card h-100 d-flex flex-column">
                        <div className="card-header bg-white border-bottom">
                            <div className="d-flex align-items-center">
                                <button
                                    className="btn btn-sm btn-outline-secondary me-3"
                                    onClick={() => navigate('/messages')}
                                >
                                    <i className="bi bi-arrow-left"></i> Back
                                </button>
                                <h5 className="mb-0">Conversation</h5>
                            </div>
                        </div>

                        <div className="card-body overflow-auto flex-grow-1">
                            {messages.length === 0 ? (
                                <div className="text-center text-muted mt-5">
                                    <i className="bi bi-chat-text display-4"></i>
                                    <p className="mt-2">No messages yet. Say hello!</p>
                                </div>
                            ) : (
                                <div>
                                    {messages.map((msg) => {
                                        const isOwn = msg.sender_id === user.id;
                                        return (
                                            <div
                                                key={msg.id}
                                                className={`d-flex mb-3 ${isOwn ? 'justify-content-end' : 'justify-content-start'}`}
                                            >
                                                <div style={{ maxWidth: '70%' }}>
                                                    {!isOwn && (
                                                        <small className="text-muted d-block mb-1">
                                                            {msg.sender_name}
                                                        </small>
                                                    )}
                                                    <div
                                                        className={`p-3 rounded ${isOwn
                                                                ? 'bg-primary text-white'
                                                                : 'bg-light text-dark'
                                                            }`}
                                                    >
                                                        <p className="mb-0">{msg.content}</p>
                                                        <small
                                                            className={`d-block mt-1 ${isOwn ? 'text-white-50' : 'text-muted'
                                                                }`}
                                                            style={{ fontSize: '0.75rem' }}
                                                        >
                                                            {formatTime(msg.created_at)}
                                                            {msg.edited_at && ' (edited)'}
                                                        </small>
                                                    </div>
                                                </div>
                                            </div>
                                        );
                                    })}
                                    <div ref={messagesEndRef} />
                                </div>
                            )}
                        </div>

                        <div className="card-footer bg-white border-top">
                            <form onSubmit={handleSend} className="d-flex gap-2">
                                <input
                                    type="text"
                                    className="form-control"
                                    placeholder="Type a message..."
                                    value={newMessage}
                                    onChange={(e) => setNewMessage(e.target.value)}
                                    disabled={sending}
                                />
                                <button
                                    type="submit"
                                    className="btn btn-primary"
                                    disabled={sending || !newMessage.trim()}
                                >
                                    {sending ? (
                                        <span className="spinner-border spinner-border-sm"></span>
                                    ) : (
                                        <i className="bi bi-send"></i>
                                    )}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatView;
