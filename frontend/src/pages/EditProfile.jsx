import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI } from '../utils/api';
import { useAuth } from '../context/AuthContext';

const EditProfile = () => {
    const { user, updateUser } = useAuth();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const [formData, setFormData] = useState({
        name: '',
        branch: '',
        year: '',
        bio: '',
        linkedin_url: '',
        github_url: ''
    });

    useEffect(() => {
        const loadProfile = async () => {
            try {
                const response = await authAPI.getCurrentUser();
                const u = response.data.user;
                setFormData({
                    name: u.name || '',
                    branch: u.branch || '',
                    year: u.year || '',
                    bio: u.bio || '',
                    linkedin_url: u.linkedin_url || '',
                    github_url: u.github_url || ''
                });
            } catch (err) {
                setError('Failed to load profile data');
            } finally {
                setLoading(false);
            }
        };
        loadProfile();
    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        setError('');
        setSuccess('');

        try {
            await authAPI.updateProfile(formData);

            // Update local user context
            if (updateUser) {
                updateUser({ ...user, ...formData });
            }

            setSuccess('Profile updated successfully!');
            setTimeout(() => {
                navigate(`/profile/${user.username}`);
            }, 1000);
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to update profile');
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="container mt-5 text-center">
                <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    return (
        <div className="container py-4">
            <div className="row">
                <div className="col-lg-8 mx-auto">
                    <div className="card border-0 shadow-sm">
                        <div className="card-body p-4 p-md-5">
                            <div className="d-flex align-items-center gap-3 mb-4 pb-3 border-bottom">
                                <div
                                    className="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center fw-bold"
                                    style={{ width: '56px', height: '56px', fontSize: '24px' }}
                                >
                                    {formData.name?.[0]?.toUpperCase() || 'U'}
                                </div>
                                <div>
                                    <h3 className="fw-bold mb-0">Edit Profile</h3>
                                    <p className="text-muted mb-0 small">Update your personal information</p>
                                </div>
                            </div>

                            {error && (
                                <div className="alert alert-danger border-0 shadow-sm py-2">{error}</div>
                            )}
                            {success && (
                                <div className="alert alert-success border-0 shadow-sm py-2">{success}</div>
                            )}

                            <form onSubmit={handleSubmit}>
                                {/* Name */}
                                <div className="mb-4">
                                    <label className="form-label fw-medium small text-muted">
                                        <i className="bi bi-person me-1"></i> Display Name
                                    </label>
                                    <input
                                        type="text"
                                        className="form-control form-control-lg border-0 bg-light"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                        placeholder="Your full name"
                                        required
                                    />
                                </div>

                                {/* Branch & Year */}
                                <div className="row g-3 mb-4">
                                    <div className="col-md-6">
                                        <label className="form-label fw-medium small text-muted">
                                            <i className="bi bi-mortarboard me-1"></i> Branch
                                        </label>
                                        <select
                                            className="form-select form-select-lg border-0 bg-light"
                                            name="branch"
                                            value={formData.branch}
                                            onChange={handleChange}
                                        >
                                            <option value="">Select Branch</option>
                                            <option value="CSE">CSE</option>
                                            <option value="ECE">ECE</option>
                                            <option value="EEE">EEE</option>
                                            <option value="Mechanical">Mechanical</option>
                                            <option value="Civil">Civil</option>
                                            <option value="IT">IT</option>
                                            <option value="AI/ML">AI/ML</option>
                                            <option value="Data Science">Data Science</option>
                                            <option value="Other">Other</option>
                                        </select>
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label fw-medium small text-muted">
                                            <i className="bi bi-calendar3 me-1"></i> Year
                                        </label>
                                        <select
                                            className="form-select form-select-lg border-0 bg-light"
                                            name="year"
                                            value={formData.year}
                                            onChange={handleChange}
                                        >
                                            <option value="">Select Year</option>
                                            <option value="1st Year">1st Year</option>
                                            <option value="2nd Year">2nd Year</option>
                                            <option value="3rd Year">3rd Year</option>
                                            <option value="4th Year">4th Year</option>
                                            <option value="Alumni">Alumni</option>
                                            <option value="Faculty">Faculty</option>
                                        </select>
                                    </div>
                                </div>

                                {/* Bio */}
                                <div className="mb-4">
                                    <label className="form-label fw-medium small text-muted">
                                        <i className="bi bi-pencil-square me-1"></i> Bio
                                    </label>
                                    <textarea
                                        className="form-control border-0 bg-light"
                                        name="bio"
                                        rows="3"
                                        value={formData.bio}
                                        onChange={handleChange}
                                        placeholder="Tell us about yourself..."
                                        maxLength={300}
                                    ></textarea>
                                    <div className="text-end small text-muted mt-1">
                                        {formData.bio.length}/300
                                    </div>
                                </div>

                                {/* Social Links */}
                                <h6 className="fw-bold text-muted small text-uppercase mb-3 mt-4">
                                    <i className="bi bi-link-45deg me-1"></i> Social Links
                                </h6>

                                <div className="mb-3">
                                    <label className="form-label fw-medium small text-muted">
                                        <i className="bi bi-linkedin me-1 text-primary"></i> LinkedIn
                                    </label>
                                    <input
                                        type="url"
                                        className="form-control border-0 bg-light"
                                        name="linkedin_url"
                                        value={formData.linkedin_url}
                                        onChange={handleChange}
                                        placeholder="https://linkedin.com/in/yourprofile"
                                    />
                                </div>

                                <div className="mb-4">
                                    <label className="form-label fw-medium small text-muted">
                                        <i className="bi bi-github me-1"></i> GitHub
                                    </label>
                                    <input
                                        type="url"
                                        className="form-control border-0 bg-light"
                                        name="github_url"
                                        value={formData.github_url}
                                        onChange={handleChange}
                                        placeholder="https://github.com/yourusername"
                                    />
                                </div>

                                {/* Buttons */}
                                <div className="d-flex gap-3 pt-3 border-top">
                                    <button
                                        type="submit"
                                        className="btn btn-primary px-4 rounded-pill"
                                        disabled={saving}
                                    >
                                        {saving ? (
                                            <>
                                                <span className="spinner-border spinner-border-sm me-2"></span>
                                                Saving...
                                            </>
                                        ) : (
                                            <>
                                                <i className="bi bi-check-lg me-1"></i> Save Changes
                                            </>
                                        )}
                                    </button>
                                    <button
                                        type="button"
                                        className="btn btn-outline-secondary px-4 rounded-pill"
                                        onClick={() => navigate(-1)}
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

export default EditProfile;
