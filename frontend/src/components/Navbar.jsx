import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const isActive = (path) => location.pathname === path;

    return (
        <nav className="navbar navbar-expand-lg sticky-top">
            <div className="container">
                <Link className="navbar-brand d-flex align-items-center gap-2" to="/">
                    <div className="d-flex align-items-center justify-content-center bg-primary text-white rounded-circle" style={{ width: '40px', height: '40px' }}>
                        <i className="bi bi-mortarboard-fill fs-5"></i>
                    </div>
                    <div className="d-flex flex-column">
                        <span>Student Discussion Forum</span>
                        <span className="fw-normal text-secondary d-none d-lg-block" style={{ fontSize: '0.75rem', marginTop: '-2px' }}>
                            A Web-based Platform for Academic Collaboration
                        </span>
                    </div>
                </Link>

                <button
                    className="navbar-toggler border-0 shadow-none"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                >
                    <i className="bi bi-list fs-1 text-primary"></i>
                </button>

                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ms-auto align-items-center gap-lg-3">
                        <li className="nav-item">
                            <Link
                                className={`nav-link px-3 ${isActive('/') ? 'text-primary fw-bold' : ''}`}
                                to="/"
                            >
                                Home
                            </Link>
                        </li>

                        {user ? (
                            <>
                                <li className="nav-item">
                                    <Link
                                        className={`nav-link px-3 ${isActive('/messages') ? 'text-primary fw-bold' : ''}`}
                                        to="/messages"
                                    >
                                        Messages
                                    </Link>
                                </li>

                                <li className="nav-item">
                                    <Link
                                        to="/create-post"
                                        className="btn btn-primary d-flex align-items-center gap-2 rounded-pill px-4"
                                    >
                                        <i className="bi bi-plus-lg"></i>
                                        <span>New Post</span>
                                    </Link>
                                </li>

                                <li className="nav-item dropdown ms-lg-2">
                                    <a
                                        className="nav-link dropdown-toggle d-flex align-items-center gap-2"
                                        href="#"
                                        role="button"
                                        data-bs-toggle="dropdown"
                                    >
                                        <div
                                            className="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center fw-bold"
                                            style={{ width: '35px', height: '35px' }}
                                        >
                                            {user.username?.[0]?.toUpperCase() || 'U'}
                                        </div>
                                    </a>
                                    <ul className="dropdown-menu dropdown-menu-end border-0 shadow-lg rounded-3 p-2">
                                        <li className="px-3 py-2 border-bottom mb-2">
                                            <div className="fw-bold">{user.name}</div>
                                            <div className="small text-muted">@{user.username}</div>
                                        </li>
                                        <li>
                                            <Link className="dropdown-item rounded-2" to={`/profile/${user.username}`}>
                                                <i className="bi bi-person me-2"></i> Profile
                                            </Link>
                                        </li>
                                        <li>
                                            <Link className="dropdown-item rounded-2" to="/edit-profile">
                                                <i className="bi bi-gear me-2"></i> Settings
                                            </Link>
                                        </li>
                                        <li><hr className="dropdown-divider" /></li>
                                        <li>
                                            <button
                                                className="dropdown-item rounded-2 text-danger"
                                                onClick={handleLogout}
                                            >
                                                <i className="bi bi-box-arrow-right me-2"></i> Logout
                                            </button>
                                        </li>
                                    </ul>
                                </li>
                            </>
                        ) : (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link fw-medium" to="/login">
                                        Log In
                                    </Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="btn btn-primary rounded-pill px-4" to="/register">
                                        Sign Up
                                    </Link>
                                </li>
                            </>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;

