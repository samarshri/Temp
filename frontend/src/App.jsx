import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import PrivateRoute from './components/PrivateRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import CreatePost from './pages/CreatePost';
import Messages from './pages/Messages';
import ChatView from './pages/ChatView';
import Profile from './pages/Profile';
import EditProfile from './pages/EditProfile';
import PostDetail from './pages/PostDetail';
import './styles/global.css';


function App() {
    return (
        <AuthProvider>
            <Router>
                <div className="App">
                    <Navbar />
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route path="/profile/:username" element={<Profile />} />
                        <Route path="/post/:id" element={<PostDetail />} />
                        <Route

                            path="/create-post"
                            element={
                                <PrivateRoute>
                                    <CreatePost />
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/messages"
                            element={
                                <PrivateRoute>
                                    <Messages />
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/messages/:conversationId"
                            element={
                                <PrivateRoute>
                                    <ChatView />
                                </PrivateRoute>
                            }
                        />
                        <Route
                            path="/edit-profile"
                            element={
                                <PrivateRoute>
                                    <EditProfile />
                                </PrivateRoute>
                            }
                        />
                    </Routes>
                </div>
            </Router>
        </AuthProvider>
    );
}

export default App;
