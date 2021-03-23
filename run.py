from flask import Flask
import asyncio

def create_app(config_filename):
    asyncio.set_event_loop(asyncio.new_event_loop())
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from Model import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    asyncio.set_event_loop(asyncio.new_event_loop())
    app = create_app("config")
    app.run(debug=True)
