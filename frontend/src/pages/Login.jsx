import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        const result = await login(email, password);

        if (result.success) {
            navigate('/');
        } else {
            setError(result.error);
        }
        setLoading(false);
    };

    return (
        <div className="container mt-5">
            <div className="row justify-content-center">
                <div className="col-md-6 col-lg-5">
                    <div className="card border-0 shadow-lg">
                        <div className="card-body p-5">
                            <div className="text-center mb-4">
                                <i className="bi bi-mortarboard-fill text-primary display-4"></i>
                                <h2 className="fw-bold mt-2">Welcome Back</h2>
                                <p className="text-muted">Login to continue to Student Discussion Forum</p>
                            </div>

                            {error && (
                                <div className="alert alert-danger border-0 shadow-sm" role="alert">
                                    <i className="bi bi-exclamation-circle me-2"></i> {error}
                                </div>
                            )}

                            <form onSubmit={handleSubmit}>
                                <div className="mb-3">
                                    <label htmlFor="email" className="form-label fw-bold small text-uppercase text-muted">Email Address</label>
                                    <input
                                        type="email"
                                        className="form-control form-control-lg bg-light border-0"
                                        id="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        placeholder="name@example.com"
                                        required
                                    />
                                </div>

                                <div className="mb-4">
                                    <div className="d-flex justify-content-between align-items-center mb-1">
                                        <label htmlFor="password" className="form-label fw-bold small text-uppercase text-muted">Password</label>
                                        <Link to="#" className="small text-decoration-none text-primary">Forgot password?</Link>
                                    </div>
                                    <input
                                        type="password"
                                        className="form-control form-control-lg bg-light border-0"
                                        id="password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        placeholder="••••••••"
                                        required
                                    />
                                </div>

                                <button
                                    type="submit"
                                    className="btn btn-primary w-100 btn-lg rounded-pill fw-bold shadow-sm"
                                    disabled={loading}
                                >
                                    {loading ? (
                                        <>
                                            <span className="spinner-border spinner-border-sm me-2"></span>
                                            Logging in...
                                        </>
                                    ) : (
                                        'Sign In'
                                    )}
                                </button>
                            </form>

                            <div className="mt-4 text-center">
                                <p className="mb-0 text-muted">
                                    Don't have an account?{' '}
                                    <Link to="/register" className="fw-bold text-primary text-decoration-none">Create Account</Link>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;

