import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor - handle errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Don't redirect if it's a login attempt that failed
        const isLoginRequest = error.config?.url?.includes('/auth/login');

        if (error.response?.status === 401 && !isLoginRequest) {
            // Token expired or invalid
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    register: (data) => api.post('/auth/register', data),
    login: (data) => api.post('/auth/login', data),
    getCurrentUser: () => api.get('/auth/me'),
    getProfile: (userId) => api.get(`/auth/profile/${userId}`),
    updateProfile: (data) => api.put('/auth/profile', data),
};

// Posts API
export const postsAPI = {
    getAll: (params) => api.get('/posts', { params }),
    getById: (id) => api.get(`/posts/${id}`),
    create: (data) => api.post('/posts', data),
    update: (id, data) => api.put(`/posts/${id}`, data),
    delete: (id) => api.delete(`/posts/${id}`),
    vote: (id, voteType) => api.post(`/posts/${id}/vote`, { vote_type: voteType }),
};

// Comments API
export const commentsAPI = {
    create: (postId, data) => api.post(`/posts/${postId}/comments`, data),
    update: (id, data) => api.put(`/comments/${id}`, data),
    delete: (id) => api.delete(`/comments/${id}`),
};

// Messages API
export const messagesAPI = {
    getConversations: () => api.get('/conversations'),
    getConversation: (id) => api.get(`/conversations/${id}`),
    startConversation: (userId) => api.post('/conversations/start', { user_id: userId }),
    sendMessage: (convId, content) => api.post(`/conversations/${convId}/messages`, { content }),
    getUnreadCount: () => api.get('/messages/unread-count'),
};

// Profiles API
export const profilesAPI = {
    getUserProfile: (username) => api.get(`/users/${username}`),
    updateProfile: (data) => api.put('/users/profile', data),
    followUser: (username) => api.post(`/users/${username}/follow`),
    unfollowUser: (username) => api.delete(`/users/${username}/follow`),
    getFollowers: (username) => api.get(`/users/${username}/followers`),
    getFollowing: (username) => api.get(`/users/${username}/following`),
    isFollowing: (username) => api.get(`/users/${username}/is-following`),
};

// AI Service API
export const aiAPI = {
    getAnswer: (postId) => api.post('/ai/answer', { post_id: postId }),
    summarize: (postId) => api.post('/ai/summarize', { post_id: postId }),
    moderate: (content) => api.post('/ai/moderate', { content }),
    enhance: (question) => api.post('/ai/enhance', { question }),
};

export default api;

