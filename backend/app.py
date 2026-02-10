"""
Student Discussion Forum - Main Application
Flask REST API with React frontend support
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
import os

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
    app.config.from_object(config_class)
    
    # Enable CORS for development
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register API blueprints
    from routes.auth import auth_bp
    from routes.posts import posts_bp
    from routes.comments import comments_bp
    from routes.ai import ai_bp
    from routes.messages import messages_bp
    from routes.profiles import profiles_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(profiles_bp)
    
    # Serve React app
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Student Discussion Forum - REST API")
    print("="*60)
    print("API Server: http://127.0.0.1:5000")
    print("React Dev Server: http://localhost:3000 (during development)")
    print("="*60 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
