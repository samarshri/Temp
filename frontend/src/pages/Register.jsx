import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
        branch: '',
        year: '',
        section: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { register } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (formData.password !== formData.confirmPassword) {
            setError('Passwords do not match');
            return;
        }

        if (formData.password.length < 6) {
            setError('Password must be at least 6 characters');
            return;
        }

        setLoading(true);

        const result = await register({
            username: formData.username,
            name: formData.name,
            email: formData.email,
            password: formData.password,
            branch: formData.branch,
            year: formData.year,
            section: formData.section
        });

        if (result.success) {
            navigate('/');
        } else {
            setError(result.error);
        }
        setLoading(false);
    };

    return (
        <div className="container mt-5 mb-5">
            <div className="row justify-content-center">
                <div className="col-md-8 col-lg-6">
                    <div className="card border-0 shadow-lg">
                        <div className="card-body p-5">
                            <div className="text-center mb-4">
                                <h2 className="fw-bold">Create Account</h2>
                                <p className="text-muted">Join the Student Discussion Forum community</p>
                            </div>

                            {error && (
                                <div className="alert alert-danger border-0 shadow-sm" role="alert">
                                    <i className="bi bi-exclamation-circle me-2"></i> {error}
                                </div>
                            )}

                            <form onSubmit={handleSubmit}>
                                <div className="mb-3">
                                    <label htmlFor="username" className="form-label fw-bold small text-uppercase text-muted">Username *</label>
                                    <input
                                        type="text"
                                        className="form-control bg-light border-0"
                                        id="username"
                                        name="username"
                                        value={formData.username}
                                        onChange={handleChange}
                                        placeholder="johndoe"
                                        required
                                    />
                                </div>

                                <div className="row mb-3">
                                    <div className="col-md-6">
                                        <label htmlFor="name" className="form-label fw-bold small text-uppercase text-muted">Full Name *</label>
                                        <input
                                            type="text"
                                            className="form-control bg-light border-0"
                                            id="name"
                                            name="name"
                                            value={formData.name}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>
                                    <div className="col-md-6">
                                        <label htmlFor="email" className="form-label fw-bold small text-uppercase text-muted">Email *</label>
                                        <input
                                            type="email"
                                            className="form-control bg-light border-0"
                                            id="email"
                                            name="email"
                                            value={formData.email}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="row mb-3">
                                    <div className="col-md-6">
                                        <label htmlFor="password" className="form-label fw-bold small text-uppercase text-muted">Password *</label>
                                        <input
                                            type="password"
                                            className="form-control bg-light border-0"
                                            id="password"
                                            name="password"
                                            value={formData.password}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>
                                    <div className="col-md-6">
                                        <label htmlFor="confirmPassword" className="form-label fw-bold small text-uppercase text-muted">Confirm *</label>
                                        <input
                                            type="password"
                                            className="form-control bg-light border-0"
                                            id="confirmPassword"
                                            name="confirmPassword"
                                            value={formData.confirmPassword}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="row mb-4">
                                    <div className="col-md-4">
                                        <label htmlFor="branch" className="form-label fw-bold small text-uppercase text-muted">Branch *</label>
                                        <select
                                            className="form-select bg-light border-0"
                                            id="branch"
                                            name="branch"
                                            value={formData.branch}
                                            onChange={handleChange}
                                            required
                                        >
                                            <option value="">Select...</option>
                                            <option value="CSE">CSE</option>
                                            <option value="IT">IT</option>
                                            <option value="ECE">ECE</option>
                                            <option value="EEE">EEE</option>
                                            <option value="Mechanical">Mechanical</option>
                                            <option value="Civil">Civil</option>
                                        </select>
                                    </div>
                                    <div className="col-md-4">
                                        <label htmlFor="year" className="form-label fw-bold small text-uppercase text-muted">Year *</label>
                                        <select
                                            className="form-select bg-light border-0"
                                            id="year"
                                            name="year"
                                            value={formData.year}
                                            onChange={handleChange}
                                            required
                                        >
                                            <option value="">Select...</option>
                                            <option value="1st Year">1st Year</option>
                                            <option value="2nd Year">2nd Year</option>
                                            <option value="3rd Year">3rd Year</option>
                                            <option value="4th Year">4th Year</option>
                                        </select>
                                    </div>
                                    <div className="col-md-4">
                                        <label htmlFor="section" className="form-label fw-bold small text-uppercase text-muted">Section</label>
                                        <input
                                            type="text"
                                            className="form-control bg-light border-0"
                                            id="section"
                                            name="section"
                                            value={formData.section}
                                            onChange={handleChange}
                                            placeholder="A"
                                        />
                                    </div>
                                </div>

                                <button
                                    type="submit"
                                    className="btn btn-primary w-100 btn-lg rounded-pill fw-bold shadow-sm"
                                    disabled={loading}
                                >
                                    {loading ? (
                                        <>
                                            <span className="spinner-border spinner-border-sm me-2"></span>
                                            Creating account...
                                        </>
                                    ) : (
                                        'Create Account'
                                    )}
                                </button>
                            </form>

                            <div className="mt-4 text-center">
                                <p className="mb-0 text-muted">
                                    Already have an account?{' '}
                                    <Link to="/login" className="fw-bold text-primary text-decoration-none">Login here</Link>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Register;

