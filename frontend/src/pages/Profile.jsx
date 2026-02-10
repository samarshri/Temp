import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { profilesAPI, messagesAPI } from '../utils/api';
import { useAuth } from '../context/AuthContext';

const Profile = () => {
    const { username } = useParams();
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const { user } = useAuth();
    const navigate = useNavigate();
    const isOwnProfile = user && user.username?.toLowerCase() === username?.toLowerCase();

    useEffect(() => {
        fetchProfile();
    }, [username]);

    const fetchProfile = async () => {
        setLoading(true);
        try {
            const response = await profilesAPI.getUserProfile(username);
            setProfile(response.data.user);
        } catch (error) {
            console.error('Error fetching profile:', error);
            setProfile(null);
        }
        setLoading(false);
    };

    const handleMessage = async () => {
        if (!profile) return;
        try {
            const response = await messagesAPI.startConversation(profile.id);
            navigate(`/messages/${response.data.conversation_id}`);
        } catch (error) {
            console.error('Error starting conversation:', error);
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

    if (!profile) {
        return (
            <div className="container mt-5">
                <div className="alert alert-info text-center">
                    <i className="bi bi-person-exclamation me-2"></i>
                    User not found or profile does not exist.
                </div>
            </div>
        );
    }

    return (
        <div className="container mt-4 pb-5">
            <div className="row">
                <div className="col-lg-8 mx-auto">
                    {/* Profile Header */}
                    <div className="card border-0 shadow-sm mb-4">
                        <div className="card-body p-4">
                            <div className="d-flex align-items-start gap-4">
                                <div>
                                    {profile.avatar_url ? (
                                        <img
                                            src={profile.avatar_url}
                                            alt={profile.name}
                                            className="rounded-circle"
                                            width="100"
                                            height="100"
                                        />
                                    ) : (
                                        <div
                                            className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center"
                                            style={{ width: '100px', height: '100px', fontSize: '40px' }}
                                        >
                                            {profile.name?.charAt(0).toUpperCase()}
                                        </div>
                                    )}
                                </div>
                                <div className="flex-grow-1">
                                    <h3 className="mb-1">{profile.display_name || profile.name}</h3>
                                    <p className="text-muted mb-2">@{profile.username}</p>

                                    {profile.status && (
                                        <p className="text-muted mb-3"><i>{profile.status}</i></p>
                                    )}

                                    <div className="mb-3">
                                        <span className="badge bg-info me-2">{profile.branch || 'No Branch'}</span>
                                        <span className="badge bg-secondary me-2">{profile.year || 'No Year'}</span>
                                        {profile.section && <span className="badge bg-secondary">Section {profile.section}</span>}
                                    </div>

                                    <div className="mb-3">
                                        <span className="me-3">
                                            <strong>{profile.followers_count}</strong> Followers
                                        </span>
                                        <span className="me-3">
                                            <strong>{profile.following_count}</strong> Following
                                        </span>
                                        <span className="me-3">
                                            <strong>{profile.posts_count}</strong> Posts
                                        </span>
                                        <span>
                                            <i className="bi bi-star-fill text-warning"></i> <strong>{profile.reputation_points}</strong> Rep
                                        </span>
                                    </div>
                                    <div className="mt-4 d-flex gap-2">
                                        {isOwnProfile ? (
                                            <button
                                                className="btn btn-outline-primary rounded-pill px-4 fw-bold"
                                                onClick={() => navigate('/edit-profile')}
                                            >
                                                <i className="bi bi-pencil me-2"></i> Edit Profile
                                            </button>
                                        ) : (
                                            user && (
                                                <button
                                                    className="btn btn-primary rounded-pill px-4 fw-bold"
                                                    onClick={handleMessage}
                                                >
                                                    <i className="bi bi-chat-dots me-2"></i> Message
                                                </button>
                                            )
                                        )}
                                    </div>
                                </div>
                            </div>

                            {profile.bio && (
                                <div className="mt-3">
                                    <p>{profile.bio}</p>
                                </div>
                            )}

                            {profile.skills && (
                                <div className="mt-3">
                                    <h6>Skills</h6>
                                    <div>
                                        {JSON.parse(profile.skills || '[]').map((skill, idx) => (
                                            <span key={idx} className="badge bg-light text-dark me-2 mb-2">
                                                {skill}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {(profile.linkedin_url || profile.github_url) && (
                                <div className="mt-3">
                                    {profile.linkedin_url && (
                                        <a
                                            href={profile.linkedin_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="btn btn-sm btn-outline-primary me-2"
                                        >
                                            <i className="bi bi-linkedin"></i> LinkedIn
                                        </a>
                                    )}
                                    {profile.github_url && (
                                        <a
                                            href={profile.github_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="btn btn-sm btn-outline-dark"
                                        >
                                            <i className="bi bi-github"></i> GitHub
                                        </a>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Activity Section */}
                    <div className="card">
                        <div className="card-header">
                            <h5 className="mb-0">Recent Activity</h5>
                        </div>
                        <div className="card-body">
                            <p className="text-muted">Activity feed coming soon...</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Profile;
