import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { messagesAPI } from '../utils/api';
import { useAuth } from '../context/AuthContext';

const Messages = () => {
    const [conversations, setConversations] = useState([]);
    const [loading, setLoading] = useState(true);
    const { user } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        fetchConversations();
    }, []);

    const fetchConversations = async () => {
        try {
            const response = await messagesAPI.getConversations();
            setConversations(response.data.conversations);
        } catch (error) {
            console.error('Error fetching conversations:', error);
        }
        setLoading(false);
    };

    const formatTime = (timestamp) => {
        if (!timestamp) return '';
        const date = new Date(timestamp);
        const now = new Date();
        const diff = now - date;

        if (diff < 86400000) { // Less than 24 hours
            return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        }
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
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
        <div className="container mt-4">
            <div className="row justify-content-center">
                <div className="col-lg-8">
                    <div className="card">
                        <div className="card-header bg-primary text-white">
                            <h4 className="mb-0"><i className="bi bi-chat-dots me-2"></i>Messages</h4>
                        </div>
                        <div className="card-body p-0">
                            {conversations.length === 0 ? (
                                <div className="text-center py-5">
                                    <i className="bi bi-inbox display-1 text-muted"></i>
                                    <p className="mt-3 text-muted">No messages yet</p>
                                </div>
                            ) : (
                                <div className="list-group list-group-flush">
                                    {conversations.map((conv) => (
                                        <div
                                            key={conv.id}
                                            className="list-group-item list-group-item-action"
                                            style={{ cursor: 'pointer' }}
                                            onClick={() => navigate(`/messages/${conv.id}`)}
                                        >
                                            <div className="d-flex align-items-center">
                                                <div className="me-3">
                                                    {conv.other_user?.avatar_url ? (
                                                        <img
                                                            src={conv.other_user.avatar_url}
                                                            alt={conv.other_user.name}
                                                            className="rounded-circle"
                                                            width="50"
                                                            height="50"
                                                        />
                                                    ) : (
                                                        <div
                                                            className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center"
                                                            style={{ width: '50px', height: '50px', fontSize: '20px' }}
                                                        >
                                                            {conv.other_user?.name?.charAt(0).toUpperCase()}
                                                        </div>
                                                    )}
                                                </div>
                                                <div className="flex-grow-1">
                                                    <div className="d-flex justify-content-between align-items-start">
                                                        <div>
                                                            <h6 className="mb-0">{conv.other_user?.name}</h6>
                                                            <small className="text-muted">@{conv.other_user?.username}</small>
                                                        </div>
                                                        <small className="text-muted">{formatTime(conv.updated_at)}</small>
                                                    </div>
                                                    {conv.unread_count > 0 && (
                                                        <span className="badge bg-primary mt-1">{conv.unread_count} new</span>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Messages;
