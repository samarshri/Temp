# Deployment Guide - Student Discussion Forum

## Quick Deploy to Render.com (Free)

### Step 1: Push to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   cd "D:\New folder (8)"
   git init
   git add .
   git commit -m "Initial commit - Student Discussion Forum"
   ```

2. **Create GitHub Repository**:
   - Go to [github.com/new](https://github.com/new)
   - Name: `student-discussion-forum`
   - Keep it Public (required for free Render)
   - Don't add README/gitignore (we already have them)
   - Click "Create repository"

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/student-discussion-forum.git
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Deploy on Render

1. **Sign up on Render**:
   - Go to [render.com](https://render.com)
   - Click "Get Started for Free"
   - Sign up with GitHub (recommended)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Click "Build and deploy from a Git repository"
   - Find and select your `student-discussion-forum` repo
   - Click "Connect"

3. **Configure Service**:
   - **Name**: `student-forum` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:create_app() --bind 0.0.0.0:$PORT`
   - **Instance Type**: `Free`

4. **Add Environment Variables**:
   Click "Advanced" and add:
   - `SECRET_KEY`: Generate a random string (e.g., use [randomkeygen.com](https://randomkeygen.com))
   - `AI_PROVIDER`: `mock` (or `openai` if you have API key)
   - If using OpenAI:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `AI_MODEL`: `gpt-3.5-turbo`

5. **Create PostgreSQL Database** (Optional but recommended):
   - Click "New +" → "PostgreSQL"
   - Name: `student-forum-db`
   - Instance Type: `Free`
   - Click "Create Database"
   - Wait for it to be created
   - Go back to your Web Service settings
   - Add environment variable:
     - `DATABASE_URL`: Copy from the PostgreSQL database "Internal Database URL"

6. **Deploy**:
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your site will be live at `https://student-forum.onrender.com` (or your chosen name)

---

### Step 3: Initial Setup After Deployment

1. **Visit your site**: `https://your-app-name.onrender.com`

2. **Login as admin**:
   - Email: `admin@forum.com`
   - Password: `admin123`
   - **Change this password immediately!**

3. **Test features**:
   - Create a discussion
   - Test AI features
   - Register a student account

---

## Alternative: Deploy to PythonAnywhere

### Step 1: Upload Files

1. **Sign up**: [pythonanywhere.com/registration](https://www.pythonanywhere.com/registration/register/beginner/)

2. **Upload code**:
   - Go to "Files" tab
   - Create folder: `student-forum`
   - Upload all your files

3. **Install dependencies**:
   - Go to "Consoles" tab
   - Start a Bash console
   - Run:
     ```bash
     cd student-forum
     pip3 install --user -r requirements.txt
     ```

### Step 2: Configure Web App

1. **Go to "Web" tab**
2. **Click "Add a new web app"**
3. **Choose**:
   - Framework: Manual configuration
   - Python version: 3.10

4. **Configure**:
   - Source code: `/home/yourusername/student-forum`
   - Working directory: `/home/yourusername/student-forum`
   - WSGI file: Edit and replace with:
     ```python
     import sys
     path = '/home/yourusername/student-forum'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import create_app
     application = create_app()
     ```

5. **Reload** and visit your site at `yourusername.pythonanywhere.com`

---

## Troubleshooting

### Issue: App won't start
- Check logs in Render dashboard
- Ensure all dependencies are in requirements.txt
- Verify DATABASE_URL is set correctly

### Issue: Database errors
- Make sure PostgreSQL database is created and connected
- Check DATABASE_URL environment variable
- Initial startup might take 30-60 seconds

### Issue: AI features not working
- Verify AI_PROVIDER is set to 'mock' (works without API key)
- If using OpenAI, check API key is correct

---

## Environment Variables Summary

| Variable | Value | Required |
|----------|-------|----------|
| SECRET_KEY | Random string | Yes |
| AI_PROVIDER | `mock` or `openai` | Yes |
| DATABASE_URL | Auto from Render PostgreSQL | Yes (production) |
| OPENAI_API_KEY | Your API key | Only if AI_PROVIDER=openai |
| AI_MODEL | `gpt-3.5-turbo` | Only if using OpenAI |

---

## Free Tier Limitations

**Render Free**:
- Sleeps after 15 min inactivity
- 750 hours/month
- Takes 30-60s to wake up
- Shared IP address

**PythonAnywhere Free**:
- Always on (no sleeping)
- 512 MB storage
- One web app only
- Subdomain only (no custom domain)

---

## Post-Deployment

✅ Your forum is now live and accessible worldwide!
✅ Share the URL with students
✅ Monitor usage in Render/PythonAnywhere dashboard
✅ Consider upgrading for custom domain and better performance

---

Need help? Check the Render docs or let me know!
