import os
import logging
from flask import Flask, jsonify, request

def create_app():
    app = Flask(__name__)

    # Configuration (no hardcoded secrets)
    app.config["APP_NAME"] = os.getenv("APP_NAME", "Secure Python App")
    app.config["ENV"] = os.getenv("ENV", "production")

    # Logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

    @app.before_request
    def log_request():
        logging.info(
            "Request received | Method=%s Path=%s RemoteAddr=%s",
            request.method,
            request.path,
            request.remote_addr
        )

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "app": app.config["APP_NAME"],
            "status": "running",
            "environment": app.config["ENV"]
        })

    @app.route("/health", methods=["GET"])
    def health():
        """
        Health check endpoint for load balancers & monitoring
        """
        return jsonify({
            "status": "healthy"
        }), 200

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logging.error("Internal server error: %s", error)
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port)
