# Student Discussion Forum

## Overview
A modern student discussion forum built with **React** frontend and **Flask REST API** backend, using **MySQL** for data persistence.

## Tech Stack

### Backend
- **Flask** - REST API framework
- **MySQL** - Database (raw SQL queries, no ORM)
- **JWT** - Authentication
- **Flask-CORS** - Cross-origin support

### Frontend
- **React 18** - UI framework
- **React Router v6** - Client-side routing
- **Axios** - HTTP client
- **Bootstrap 5** - Styling
- **Context API** - State management

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### 1. Database Setup
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE forum_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env file with your MySQL credentials
DATABASE_URL=mysql://username:password@localhost/forum_db
SECRET_KEY=your-secret-key

# Initialize database
python init_db.py
# Type 'yes' when prompted

# Run Flask API
python app.py
# API runs on http://localhost:5000
```

### 3. Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
# App runs on http://localhost:3000
```

## Features

✅ **User Authentication** - JWT-based login/register
✅ **Discussion Posts** - Create, read, update, delete
✅ **Search & Filter** - By subject, keyword
✅ **Sorting** - Latest, Top, Most Active
✅ **User Profiles** - Bio, major, year, social links
✅ **Protected Routes** - Authentication required for certain actions

### Coming Soon
- Post detail page with comments
- Voting (upvote/downvote)
- Threaded comments
- AI features (answer assistant, moderation)

## Project Structure

```
.
├── backend/
│   ├── models/          # Raw MySQL models
│   ├── routes/          # API endpoints
│   ├── app.py           # Flask app
│   ├── auth_middleware.py
│   ├── db.py            # Database utilities
│   └── schema.sql       # Database schema
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/  # Reusable components
    │   ├── pages/       # Page components
    │   ├── context/     # React context
    │   └── utils/       # API utilities
    └── package.json
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `GET /api/auth/profile/:id` - Get user profile
- `PUT /api/auth/profile` - Update profile

### Posts
- `GET /api/posts` - Get all posts (with filters)
- `GET /api/posts/:id` - Get single post
- `POST /api/posts` - Create post (auth required)
- `PUT /api/posts/:id` - Update post (auth required)
- `DELETE /api/posts/:id` - Delete post (auth required)
- `POST /api/posts/:id/vote` - Vote on post (auth required)

### Comments
- `POST /api/posts/:id/comments` - Add comment (auth required)
- `PUT /api/comments/:id` - Update comment (auth required)
- `DELETE /api/comments/:id` - Delete comment (auth required)

## Development

### Backend
```bash
python app.py
```

### Frontend
```bash
cd frontend
npm start
```

### Production Build
```bash
cd frontend
npm run build
# Flask will serve the built files
```

## License
MIT
