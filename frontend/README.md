# Student Discussion Forum - React Frontend

## Setup Instructions

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm start
```
The React app will run on http://localhost:3000

### 3. Start Flask Backend (in separate terminal)
```bash
# First, configure MySQL in .env
# Then install Python dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run Flask API
python app.py
```
Flask API will run on http://localhost:5000

## Project Structure
```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Navbar.jsx
│   │   ├── PostCard.jsx
│   │   └── PrivateRoute.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   └── CreatePost.jsx
│   ├── context/
│   │   └── AuthContext.jsx
│   ├── utils/
│   │   └── api.js
│   ├── styles/
│   │   └── global.css
│   ├── App.jsx
│   └── index.js
└── package.json
```

## Features Implemented
✅ User Authentication (JWT)
✅ Home Feed with Posts
✅ Search and Filtering
✅ Sort by Latest/Top/Most Active
✅ Create New Discussion
✅ Protected Routes

## Still To Implement
- Post Detail Page with Comments
- Voting Functionality
- User Profile Pages
- Edit/Delete Posts
- Comment Threading

## Technologies
- React 18
- React Router v6
- Axios for API calls
- Bootstrap 5
- Context API for state management
