from flask import Flask
from config import SECRET_KEY, UPLOAD_FOLDER
from routes.analyze import analyze_bp
from utils.logger import logger


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

    app.register_blueprint(analyze_bp)

    logger.info("Upfolio backend ready — uploads go to %s", UPLOAD_FOLDER)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
