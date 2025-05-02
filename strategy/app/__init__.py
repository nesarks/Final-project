from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register your main routes
    from .routes import main
    app.register_blueprint(main)

    # Initialize APScheduler
    from .services.scheduler import init_scheduler
    init_scheduler()

    return app
