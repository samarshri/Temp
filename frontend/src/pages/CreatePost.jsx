import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { postsAPI, aiAPI } from '../utils/api';

const CreatePost = () => {
    const [formData, setFormData] = useState({
        title: '',
        content: '',
        subject: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [enhancing, setEnhancing] = useState(false);
    const navigate = useNavigate();

    const subjects = ['Coding', 'Studies', 'General', 'Placement', 'Projects',
        'Resources', 'Internships', 'Hackathons', 'Clubs'];

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleEnhance = async () => {
        if (!formData.content || formData.content.length < 10) {
            setError('Please write at least 10 characters to enhance.');
            return;
        }

        setEnhancing(true);
        setError('');
        try {
            const response = await aiAPI.enhance(formData.content);
            if (response.data.enhanced_question) {
                setFormData(prev => ({
                    ...prev,
                    content: response.data.enhanced_question
                }));
            }
        } catch (error) {
            console.error('Enhance error:', error);
            setError('Failed to enhance content. Please try again.');
        } finally {
            setEnhancing(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!formData.title || !formData.content || !formData.subject) {
            setError('All fields are required');
            return;
        }

        setLoading(true);
        try {
            const response = await postsAPI.create(formData);
            navigate(`/post/${response.data.post.id}`);
        } catch (error) {
            setError(error.response?.data?.error || 'Failed to create post');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container py-5">
            <div className="row justify-content-center">
                <div className="col-lg-8">
                    <div className="card shadow-md border-0">
                        <div className="card-body p-5">
                            <h2 className="mb-4 fw-bold">
                                <span className="text-gradient">Start a Discussion</span>
                            </h2>

                            {error && (
                                <div className="alert alert-danger rounded-3 border-0 shadow-sm" role="alert">
                                    <i className="bi bi-exclamation-circle me-2"></i> {error}
                                </div>
                            )}

                            <form onSubmit={handleSubmit}>
                                <div className="mb-4">
                                    <label htmlFor="title" className="form-label fw-bold">Title</label>
                                    <input
                                        type="text"
                                        className="form-control form-control-lg"
                                        id="title"
                                        name="title"
                                        value={formData.title}
                                        onChange={handleChange}
                                        placeholder="What's your question about?"
                                        required
                                    />
                                </div>

                                <div className="mb-4">
                                    <label htmlFor="subject" className="form-label fw-bold">Subject</label>
                                    <select
                                        className="form-select"
                                        id="subject"
                                        name="subject"
                                        value={formData.subject}
                                        onChange={handleChange}
                                        required
                                    >
                                        <option value="">Select a category...</option>
                                        {subjects.map((s) => (
                                            <option key={s} value={s}>{s}</option>
                                        ))}
                                    </select>
                                </div>

                                <div className="mb-4">
                                    <div className="d-flex justify-content-between align-items-center mb-2">
                                        <label htmlFor="content" className="form-label fw-bold mb-0">Content</label>
                                        <button
                                            type="button"
                                            className="btn btn-sm btn-outline-primary d-flex align-items-center gap-2"
                                            onClick={handleEnhance}
                                            disabled={enhancing || !formData.content}
                                        >
                                            {enhancing ? (
                                                <span className="spinner-border spinner-border-sm"></span>
                                            ) : (
                                                <i className="bi bi-magic"></i>
                                            )}
                                            Enhance with AI
                                        </button>
                                    </div>
                                    <textarea
                                        className="form-control"
                                        id="content"
                                        name="content"
                                        rows="8"
                                        value={formData.content}
                                        onChange={handleChange}
                                        placeholder="Describe your question or topic in detail..."
                                        style={{ resize: 'none' }}
                                        required
                                    ></textarea>
                                    <div className="form-text text-muted">
                                        Tip: Use "Enhance with AI" to improve clarity and formatting.
                                    </div>
                                </div>

                                <div className="d-flex gap-3 pt-3">
                                    <button
                                        type="submit"
                                        className="btn btn-primary px-5 rounded-pill"
                                        disabled={loading}
                                    >
                                        {loading ? (
                                            <>
                                                <span className="spinner-border spinner-border-sm me-2"></span>
                                                Publishing...
                                            </>
                                        ) : (
                                            <>Publish Discussion</>
                                        )}
                                    </button>
                                    <button
                                        type="button"
                                        className="btn btn-light px-4 rounded-pill"
                                        onClick={() => navigate('/')}
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CreatePost;

