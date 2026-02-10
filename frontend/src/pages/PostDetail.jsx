import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { postsAPI, aiAPI, commentsAPI } from '../utils/api';
import { useAuth } from '../context/AuthContext';

const PostDetail = () => {
    const { id } = useParams();
    const { user } = useAuth();
    const [post, setPost] = useState(null);
    const [comments, setComments] = useState([]);
    const [newComment, setNewComment] = useState('');
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);

    // AI States
    const [aiAnswer, setAiAnswer] = useState(null);
    const [aiSummary, setAiSummary] = useState(null);
    const [loadingAI, setLoadingAI] = useState(false);
    const [loadingSummary, setLoadingSummary] = useState(false);

    useEffect(() => {
        const fetchPostData = async () => {
            try {
                const response = await postsAPI.getById(id);
                setPost(response.data.post);
                setComments(response.data.comments || []);
                // If there's an existing AI answer/summary in the DB, we could load it here
                // For now, these are generated on demand
            } catch (error) {
                console.error('Error fetching post:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchPostData();
    }, [id]);

    const handleGetAIAnswer = async () => {
        setLoadingAI(true);
        try {
            const response = await aiAPI.getAnswer(id);
            setAiAnswer(response.data.answer);
        } catch (error) {
            console.error('Error getting AI answer:', error);
        } finally {
            setLoadingAI(false);
        }
    };

    const handleSummarize = async () => {
        setLoadingSummary(true);
        try {
            const response = await aiAPI.summarize(id);
            setAiSummary(response.data.summary);
        } catch (error) {
            console.error('Error summarizing thread:', error);
        } finally {
            setLoadingSummary(false);
        }
    };

    const handleSubmitComment = async (e) => {
        e.preventDefault();
        if (!newComment.trim()) return;

        setSubmitting(true);
        try {
            // Check moderation first (optional but good practice)
            // const modResponse = await aiAPI.moderate(newComment);
            // if (modResponse.data.flagged) { alert('Content flagged!'); return; }

            const response = await commentsAPI.create(id, { content: newComment });
            setComments([...comments, response.data.comment]);
            setNewComment('');
        } catch (error) {
            console.error('Error submitting comment:', error);
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) {
        return (
            <div className="spinner-overlay">
                <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    if (!post) {
        return <div className="container mt-5"><h3>Post not found</h3></div>;
    }

    return (
        <div className="container py-4">
            <div className="row">
                <div className="col-lg-8 mx-auto">
                    {/* Post Content */}
                    <div className="card mb-4 border-0 shadow-sm">
                        <div className="card-body p-4">
                            <div className="mb-3">
                                <span className="badge bg-light text-primary border border-primary-subtle rounded-pill px-3 py-2 fw-medium">
                                    {post.subject}
                                </span>
                            </div>

                            <h1 className="h2 fw-bold mb-3">{post.title}</h1>

                            <div className="d-flex align-items-center mb-4 text-muted small">
                                <div
                                    className="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center me-2"
                                    style={{ width: '32px', height: '32px' }}
                                >
                                    {post.author?.name?.[0]?.toUpperCase() || 'U'}
                                </div>
                                <span className="fw-medium text-dark me-2">{post.author?.name}</span>
                                <span className="me-2">•</span>
                                <span>{new Date(post.timestamp).toLocaleDateString()}</span>
                            </div>

                            <div className="post-content mb-4 text-secondary">
                                {post.content.split('\n').map((para, idx) => (
                                    <p key={idx}>{para}</p>
                                ))}
                            </div>

                            {/* AI Buttons */}
                            <div className="d-flex gap-2 flex-wrap mb-4">
                                <button
                                    onClick={handleGetAIAnswer}
                                    className="btn btn-outline-primary d-flex align-items-center gap-2"
                                    disabled={loadingAI}
                                >
                                    {loadingAI ? (
                                        <span className="spinner-border spinner-border-sm"></span>
                                    ) : (
                                        <i className="bi bi-robot"></i>
                                    )}
                                    Get AI Answer
                                </button>

                                <button
                                    onClick={handleSummarize}
                                    className="btn btn-outline-secondary d-flex align-items-center gap-2"
                                    disabled={loadingSummary}
                                >
                                    {loadingSummary ? (
                                        <span className="spinner-border spinner-border-sm"></span>
                                    ) : (
                                        <i className="bi bi-card-text"></i>
                                    )}
                                    Summarize Thread
                                </button>
                            </div>

                            {/* AI Results */}
                            {aiAnswer && (
                                <div className="ai-suggestion mb-4">
                                    <div className="ai-badge mb-2">
                                        <i className="bi bi-robot"></i> AI Answer
                                    </div>
                                    <p className="mb-0 text-dark">{aiAnswer}</p>
                                </div>
                            )}

                            {aiSummary && (
                                <div className="ai-suggestion mb-4 bg-light border-secondary">
                                    <div className="ai-badge bg-secondary mb-2">
                                        <i className="bi bi-card-text"></i> Thread Summary
                                    </div>
                                    <p className="mb-0 text-dark">{aiSummary}</p>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Comments Section */}
                    <div>
                        <h4 className="fw-bold mb-4">Comments ({comments.length})</h4>

                        {comments.length === 0 ? (
                            <div className="text-center py-4 text-muted bg-white rounded-3 mb-4 border">
                                No comments yet. Be the first to share your thoughts!
                            </div>
                        ) : (
                            <div className="d-flex flex-column gap-3 mb-4">
                                {comments.map((comment) => (
                                    <div key={comment.id} className="card border-0 shadow-sm">
                                        <div className="card-body p-3">
                                            <div className="d-flex justify-content-between align-items-center mb-2">
                                                <div className="d-flex align-items-center gap-2">
                                                    <div
                                                        className="bg-light text-secondary rounded-circle d-flex align-items-center justify-content-center small fw-bold"
                                                        style={{ width: '28px', height: '28px' }}
                                                    >
                                                        {comment.author?.name?.[0]?.toUpperCase() || 'U'}
                                                    </div>
                                                    <span className="fw-medium small">{comment.author?.name}</span>
                                                </div>
                                                <span className="text-muted small">
                                                    {new Date(comment.timestamp).toLocaleDateString()}
                                                </span>
                                            </div>
                                            <p className="mb-0 text-secondary small">{comment.content}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {user ? (
                            <div className="card border-0 shadow-sm">
                                <div className="card-body">
                                    <h5 className="card-title h6 mb-3">Leave a comment</h5>
                                    <form onSubmit={handleSubmitComment}>
                                        <div className="mb-3">
                                            <textarea
                                                className="form-control"
                                                rows="3"
                                                placeholder="What are your thoughts?"
                                                value={newComment}
                                                onChange={(e) => setNewComment(e.target.value)}
                                                required
                                            ></textarea>
                                        </div>
                                        <button
                                            type="submit"
                                            className="btn btn-primary btn-sm px-4"
                                            disabled={submitting}
                                        >
                                            {submitting ? 'Posting...' : 'Post Comment'}
                                        </button>
                                    </form>
                                </div>
                            </div>
                        ) : (
                            <div className="alert alert-info border-0 shadow-sm">
                                Please <Link to="/login" className="fw-bold">login</Link> to join the discussion.
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PostDetail;
