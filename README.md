# Student Discussion Forum

A full-stack web application built with Flask, SQLAlchemy, and AI integration for enhanced student learning and collaboration.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap_5-purple)

## ✨ Features

### Core Functionality
- 🔐 **User Authentication**: Secure registration and login with password hashing
- 💬 **Discussion Forum**: Create, view, edit, and delete discussion topics
- 📝 **Comments & Replies**: Engage in threaded discussions
- 🔍 **Search & Filter**: Find discussions by keyword, subject, or activity
- 👥 **Role-Based Access**: Admin can moderate all content

### AI-Powered Features
- 🤖 **AI Answer Assistant**: Get AI-generated answers for any discussion
- 🛡️ **Content Moderation**: Automatic spam and abuse detection
- 📊 **Thread Summarizer**: Generate summaries of long discussions
- ✨ **Question Enhancer**: Improve clarity of student questions

### Additional Features
- 📱 Responsive design (mobile-friendly)
- 🎨 Modern, clean UI with Bootstrap 5
- ⚡ Real-time validation and feedback
- 🔔 Flash messages for user actions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "D:\New folder (8)"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and go to: `http://127.0.0.1:5000`

### Default Admin Account
- **Email**: `admin@forum.com`
- **Password**: `admin123`

⚠️ **Important**: Change the admin password after first login!

## 📁 Project Structure

```
student-forum/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # SQLAlchemy database models
├── ai_service.py          # AI integration module
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── forum.db              # SQLite database (auto-created)
│
├── routes/               # Application routes
│   ├── __init__.py
│   ├── auth.py          # Authentication endpoints
│   ├── posts.py         # Discussion CRUD operations
│   ├── comments.py      # Comment management
│   └── ai.py            # AI feature APIs
│
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── login.html
│   ├── register.html
│   ├── index.html      # Discussions list
│   ├── post.html       # Single post view
│   ├── create_post.html
│   ├── edit_post.html
│   ├── 404.html
│   └── 500.html
│
└── static/             # Static files
    ├── css/
    │   └── style.css   # Custom styles
    └── js/
        └── main.js     # JavaScript functionality
```

## 🗄️ Database Schema

### Users Table
- `id`: Primary key
- `name`: User's full name
- `email`: Unique email (login identifier)
- `password_hash`: Hashed password
- `role`: 'student' or 'admin'
- `created_at`: Registration timestamp

### Posts Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `title`: Discussion title
- `content`: Discussion content
- `subject`: Subject/category tag
- `timestamp`: Creation time
- `edited_at`: Last edit time
- `view_count`: Number of views

### Comments Table
- `id`: Primary key
- `post_id`: Foreign key to Posts
- `user_id`: Foreign key to Users
- `content`: Comment text
- `timestamp`: Creation time
- `edited_at`: Last edit time

## 🔌 API Endpoints

### Authentication
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Discussions
- `GET /` - View all discussions
- `GET/POST /post/create` - Create new discussion
- `GET /post/<id>` - View single post
- `POST /post/<id>/edit` - Edit post (owner only)
- `POST /post/<id>/delete` - Delete post (owner/admin)

### Comments
- `POST /post/<id>/comment` - Add comment
- `POST /comment/<id>/edit` - Edit comment (owner only)
- `POST /comment/<id>/delete` - Delete comment (owner/admin)

### AI Features (REST API)
- `POST /ai/answer` - Get AI answer for discussion
  ```json
  {
    "post_id": 1
  }
  ```

- `POST /ai/moderate` - Check content for spam/abuse
  ```json
  {
    "content": "text to moderate"
  }
  ```

- `POST /ai/summarize` - Summarize discussion thread
  ```json
  {
    "post_id": 1
  }
  ```

- `POST /ai/enhance` - Enhance question quality
  ```json
  {
    "question": "original question text"
  }
  ```

## 🤖 AI Configuration

The application supports multiple AI providers:

### Mock AI (Default - No API Key Required)
Works out of the box with simulated responses. Perfect for development and testing.

### OpenAI Integration
1. Create a `.env` file (copy from `.env.example`)
2. Add your OpenAI API key:
   ```
   AI_PROVIDER=openai
   OPENAI_API_KEY=your-api-key-here
   AI_MODEL=gpt-3.5-turbo
   ```

### Environment Variables
- `SECRET_KEY`: Flask session secret
- `DATABASE_URL`: Database connection string (optional)
- `AI_PROVIDER`: `mock` or `openai`
- `OPENAI_API_KEY`: Your OpenAI API key
- `AI_MODEL`: Model to use (e.g., `gpt-3.5-turbo`)

## 🎨 Usage Guide

### For Students
1. **Register an account** with your email
2. **Browse discussions** on the home page
3. **Search and filter** by subject or keyword
4. **Create new discussions** with clear titles
5. **Use AI features**:
   - Click "Enhance with AI" when creating posts
   - Click "Ask AI" on any discussion for answers
   - Click "Check with AI" before posting comments
6. **Participate** by adding thoughtful replies

### For Administrators
- Access granted to `admin@forum.com`
- Can delete any post or comment
- Moderate content across all discussions
- Admin badge visible in navigation

## 🔒 Security Features

- ✅ Password hashing with Werkzeug
- ✅ Session-based authentication
- ✅ CSRF protection (Flask default)
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Role-based access control
- ✅ Content validation

## 🛠️ Development

### Running in Debug Mode
Debug mode is enabled by default when running `app.py` directly:
```bash
python app.py
```

### Database Management
The database is automatically created on first run. To reset:
```bash
# Delete the database file
rm forum.db  # or del forum.db on Windows

# Restart the application to recreate
python app.py
```

### Adding New Subjects
Edit `SUBJECTS` list in `routes/posts.py`:
```python
SUBJECTS = ['Mathematics', 'Science', 'History', 'Your Subject', ...]
```

## 📝 License

This project is created for educational purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your needs!

## 📞 Support

For issues or questions:
1. Check the code comments in `app.py`
2. Review the database schema in `models.py`
3. Test AI features with mock provider first

## 🎯 Future Enhancements

- [ ] User profiles with avatars
- [ ] Email notifications
- [ ] File attachments
- [ ] Discussion voting/rating
- [ ] Advanced search with filters
- [ ] Real-time updates with WebSockets
- [ ] Export discussions to PDF
- [ ] Integration with more LLM providers

---

**Built with ❤️ using Flask, SQLAlchemy, and AI**
