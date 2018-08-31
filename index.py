import json

from app import create_app

if __name__ == '__main__':
    with open('config.json') as f:
        app = create_app(json.load(f))
    app.run(**app.config["RUN"])
