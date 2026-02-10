import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { postsAPI } from '../utils/api';
import { useAuth } from '../context/AuthContext';

const PostCard = ({ post }) => {
    const { user } = useAuth();
    const [score, setScore] = useState(post.score || 0);
    const [userVote, setUserVote] = useState(post.user_vote || 0); // 1, -1, or 0
    const [voting, setVoting] = useState(false);

    const handleVote = async (voteType) => {
        if (!user) {
            return; // Must be logged in
        }
        if (voting) return;

        setVoting(true);
        try {
            const response = await postsAPI.vote(post.id, voteType);
            setScore(response.data.score);
            // Toggle: if same vote clicked again, it removes the vote
            setUserVote(userVote === voteType ? 0 : voteType);
        } catch (error) {
            console.error('Error voting:', error);
        } finally {
            setVoting(false);
        }
    };

    return (
        <div className="card post-card mb-4 border-0 shadow-sm">
            <div className="card-body p-4">
                <div className="d-flex gap-3">
                    {/* Voting */}
                    <div className="d-flex flex-column align-items-center vote-container h-100">
                        <i
                            className={`bi bi-caret-up-fill vote-btn fs-4 ${userVote === 1 ? 'active text-primary' : ''}`}
                            onClick={() => handleVote(1)}
                            style={{ cursor: user ? 'pointer' : 'default' }}
                            title={user ? 'Upvote' : 'Login to vote'}
                        ></i>
                        <span className="fw-bold my-1 text-primary">{score}</span>
                        <i
                            className={`bi bi-caret-down-fill vote-btn fs-4 ${userVote === -1 ? 'active text-danger' : ''}`}
                            onClick={() => handleVote(-1)}
                            style={{ cursor: user ? 'pointer' : 'default' }}
                            title={user ? 'Downvote' : 'Login to vote'}
                        ></i>
                    </div>

                    {/* Content */}
                    <div className="flex-grow-1">
                        <div className="mb-2">
                            <span className="badge bg-light text-primary border border-primary-subtle rounded-pill px-3 py-2 fw-medium">
                                {post.subject}
                            </span>
                        </div>

                        <Link to={`/post/${post.id}`} className="text-decoration-none text-dark">
                            <h4 className="card-title fw-bold mb-2">{post.title}</h4>
                            <p className="card-text text-secondary mb-3" style={{
                                display: '-webkit-box',
                                WebkitLineClamp: '3',
                                WebkitBoxOrient: 'vertical',
                                overflow: 'hidden'
                            }}>
                                {post.content}
                            </p>
                        </Link>

                        <div className="d-flex align-items-center justify-content-between mt-3 pt-3 border-top">
                            <div className="d-flex align-items-center gap-3">
                                <Link to={`/profile/${post.author?.username || post.author?.id}`} className="d-flex align-items-center text-decoration-none">
                                    <div
                                        className="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-2 small"
                                        style={{ width: '24px', height: '24px', fontSize: '10px' }}
                                    >
                                        {post.author?.name?.[0]?.toUpperCase() || 'U'}
                                    </div>
                                    <span className="text-dark fw-medium small">{post.author?.name || 'Unknown'}</span>
                                </Link>
                                <span className="text-muted small">•</span>
                                <span className="text-muted small">
                                    {new Date(post.timestamp).toLocaleDateString(undefined, {
                                        month: 'short', day: 'numeric'
                                    })}
                                </span>
                            </div>

                            <div className="d-flex align-items-center gap-3 text-muted">
                                <span className="d-flex align-items-center gap-1 small">
                                    <i className="bi bi-chat-dots"></i>
                                    {post.comment_count || 0} comments
                                </span>
                                <button
                                    className="btn btn-link text-muted p-0 text-decoration-none small"
                                    onClick={() => {
                                        navigator.clipboard.writeText(
                                            `${window.location.origin}/post/${post.id}`
                                        );
                                        alert('Link copied to clipboard!');
                                    }}
                                >
                                    <i className="bi bi-share"></i> Share
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PostCard;
