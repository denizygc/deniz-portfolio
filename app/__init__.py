from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Blueprint registration
    from app.main.routes import main_bp
    from app.projects.routes import projects_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(projects_bp, url_prefix='/projects')
    
    # Healthcheck route
    @app.route("/healthcheck")
    def healthcheck():
        return {"status": "ok"}, 200

    return app
