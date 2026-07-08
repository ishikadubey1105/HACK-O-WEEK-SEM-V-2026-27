from flask import Flask, jsonify, render_template
from app.config import Config
from app.extensions import db


def create_app():
    """Application factory — creates and configures the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register route blueprints
    from app.routes.books   import books_bp
    from app.routes.members import members_bp
    from app.routes.borrow  import borrow_bp

    app.register_blueprint(books_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(borrow_bp)

    # Create all database tables on startup
    with app.app_context():
        db.create_all()

    # Welcome route — shows all available endpoints
    @app.route("/")
    def index():
        # Serve the beautiful HTML frontend
        return render_template("index.html")

    @app.route("/api")
    def api_info():
        # Keep a JSON info endpoint at /api for Postman users
        return jsonify({
            "message": "Library Management System API",
            "version": "1.0",
            "frontend": "Visit http://127.0.0.1:5000/ for the web UI",
        }), 200

    # Custom 404 error handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": str(error)}), 404

    # Custom 405 error handler
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"success": False, "error": "Method not allowed"}), 405

    return app
