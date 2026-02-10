import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { postsAPI } from '../utils/api';
import PostCard from '../components/PostCard';
import { useAuth } from '../context/AuthContext';

const Home = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [subject, setSubject] = useState('');
    const [sortBy, setSortBy] = useState('latest');
    const { user } = useAuth();
    const navigate = useNavigate();

    const categoryGroups = [
        {
            label: 'Academic',
            icon: 'bi-mortarboard',
            items: [
                { name: 'Coding', icon: 'bi-code-slash' },
                { name: 'Studies', icon: 'bi-book' },
                { name: 'Projects', icon: 'bi-kanban' },
                { name: 'Resources', icon: 'bi-folder2-open' },
            ]
        },
        {
            label: 'Career',
            icon: 'bi-briefcase',
            items: [
                { name: 'Internships', icon: 'bi-building' },
                { name: 'Placement', icon: 'bi-graph-up-arrow' },
            ]
        },
        {
            label: 'Community',
            icon: 'bi-people',
            items: [
                { name: 'Clubs', icon: 'bi-star' },
                { name: 'Hackathons', icon: 'bi-trophy' },
                { name: 'General Discussion', icon: 'bi-chat-left-text' },
            ]
        }
    ];

    const fetchPosts = async () => {
        setLoading(true);
        try {
            const response = await postsAPI.getAll({ search, subject, sort: sortBy });
            setPosts(response.data.posts);
        } catch (error) {
            console.error('Error fetching posts:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPosts();
    }, [sortBy, subject]);

    const handleSearch = (e) => {
        e.preventDefault();
        fetchPosts();
    };

    return (
        <div className="container py-4">
            <div className="row g-4">
                {/* Left Sidebar - Navigation & Filters */}
                <div className="col-lg-3 d-none d-lg-block">
                    <div className="card border-0 shadow-sm sticky-top" style={{ top: '90px' }}>
                        <div className="card-body p-4">
                            {!user && (
                                <div className="mb-4 pb-4 border-bottom">
                                    <h5 className="fw-bold mb-3">Join the Community</h5>
                                    <p className="text-muted small mb-3">Connect with students, ask questions, and share knowledge.</p>
                                    <div className="d-grid gap-2">
                                        <button onClick={() => navigate('/register')} className="btn btn-primary rounded-pill btn-sm">Sign Up</button>
                                        <button onClick={() => navigate('/login')} className="btn btn-outline-primary rounded-pill btn-sm">Log In</button>
                                    </div>
                                </div>
                            )}

                            <h6 className="fw-bold text-uppercase text-muted small mb-3">Sort By</h6>
                            <div className="nav flex-column mb-4 nav-pills">
                                <button
                                    className={`nav-link text-start ${sortBy === 'latest' ? 'active bg-primary-subtle text-primary fw-bold' : 'text-secondary'}`}
                                    onClick={() => setSortBy('latest')}
                                >
                                    <i className="bi bi-clock me-2"></i> Latest
                                </button>
                                <button
                                    className={`nav-link text-start ${sortBy === 'top' ? 'active bg-primary-subtle text-primary fw-bold' : 'text-secondary'}`}
                                    onClick={() => setSortBy('top')}
                                >
                                    <i className="bi bi-graph-up-arrow me-2"></i> Top Rated
                                </button>
                                <button
                                    className={`nav-link text-start ${sortBy === 'most_active' ? 'active bg-primary-subtle text-primary fw-bold' : 'text-secondary'}`}
                                    onClick={() => setSortBy('most_active')}
                                >
                                    <i className="bi bi-fire me-2"></i> Most Active
                                </button>
                            </div>

                            <h6 className="fw-bold text-uppercase text-muted small mb-3">Topics</h6>
                            <div className="nav flex-column nav-pills">
                                <button
                                    className={`nav-link text-start ${subject === '' ? 'active bg-primary-subtle text-primary fw-bold' : 'text-secondary'}`}
                                    onClick={() => setSubject('')}
                                >
                                    <i className="bi bi-grid-3x3-gap me-2"></i> All Topics
                                </button>

                                {categoryGroups.map(group => (
                                    <div key={group.label} className="mt-3">
                                        <div className="d-flex align-items-center gap-2 mb-1 px-2">
                                            <i className={`bi ${group.icon} text-muted`} style={{ fontSize: '0.7rem' }}></i>
                                            <span className="text-uppercase text-muted fw-semibold" style={{ fontSize: '0.65rem', letterSpacing: '0.08em' }}>
                                                {group.label}
                                            </span>
                                        </div>
                                        {group.items.map(cat => (
                                            <button
                                                key={cat.name}
                                                className={`nav-link text-start py-2 ${subject === cat.name ? 'active bg-primary-subtle text-primary fw-bold' : 'text-secondary'}`}
                                                onClick={() => setSubject(cat.name)}
                                            >
                                                <i className={`bi ${cat.icon} me-2`} style={{ fontSize: '0.85rem' }}></i>
                                                {cat.name}
                                            </button>
                                        ))}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Main Feed */}
                <div className="col-lg-6">
                    {/* Search Bar */}
                    <div className="mb-4">
                        <form onSubmit={handleSearch} className="position-relative">
                            <i className="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                            <input
                                type="text"
                                className="form-control form-control-lg ps-5 rounded-pill border-0 shadow-sm"
                                placeholder="Search discussions..."
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                            />
                        </form>
                    </div>

                    {/* Posts */}
                    {loading ? (
                        <div className="text-center py-5">
                            <div className="spinner-border text-primary" role="status">
                                <span className="visually-hidden">Loading...</span>
                            </div>
                        </div>
                    ) : posts.length === 0 ? (
                        <div className="text-center py-5">
                            <img src="https://via.placeholder.com/150?text=No+Posts" alt="No posts" className="mb-3 opacity-50 rounded" />
                            <h4 className="text-muted">No discussions found</h4>
                            <p className="text-muted">Be the first to start a conversation!</p>
                            {user && (
                                <button onClick={() => navigate('/create-post')} className="btn btn-primary mt-2">
                                    Start Discussion
                                </button>
                            )}
                        </div>
                    ) : (
                        posts.map((post) => <PostCard key={post.id} post={post} />)
                    )}
                </div>

                {/* Right Sidebar - Trending/Extras */}
                <div className="col-lg-3 d-none d-lg-block">
                    <div className="sticky-top" style={{ top: '90px' }}>
                        {/* Create Post Button (Mobile/Tablet usually, but kept here for easy access) */}
                        {user && (
                            <button
                                onClick={() => navigate('/create-post')}
                                className="btn btn-primary w-100 rounded-pill mb-4 py-2 fw-bold shadow-sm"
                            >
                                <i className="bi bi-plus-lg me-2"></i> Start Discussion
                            </button>
                        )}

                        <div className="card border-0 shadow-sm mb-4">
                            <div className="card-body">
                                <h6 className="fw-bold mb-3">About the Forum</h6>
                                <p className="small text-secondary mb-0">
                                    A central place for students to discuss coursework, share resources, and connect with peers within the academic community.
                                </p>
                            </div>
                        </div>

                        <div className="card border-0 shadow-sm">
                            <div className="card-body">
                                <h6 className="fw-bold mb-3">Guidelines</h6>
                                <ul className="list-unstyled small text-secondary mb-0 d-flex flex-column gap-2">
                                    <li><i className="bi bi-person-check text-muted me-2"></i>Maintain academic integrity</li>
                                    <li><i className="bi bi-chat-left-dots text-muted me-2"></i>Be respectful to peers</li>
                                    <li><i className="bi bi-tag text-muted me-2"></i>Use appropriate topic filters</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;

