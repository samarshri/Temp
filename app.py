"""
Student Discussion Forum - Main Application
Flask web application with AI integration for educational discussions
"""

from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.posts import posts_bp
    from routes.comments import comments_bp
    from routes.ai import ai_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(ai_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(email='admin@forum.com').first()
        if not admin:
            admin = User(name='Admin', email='admin@forum.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: admin@forum.com / admin123")
    
    return app


if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*60)
    print("Student Discussion Forum - AI Enhanced")
    print("="*60)
    print("Server starting at: http://127.0.0.1:5000")
    print("Default Admin: admin@forum.com / admin123")
    print("="*60 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
