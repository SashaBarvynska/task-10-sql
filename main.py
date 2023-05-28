import src.routes  # NOQA
from config import Config
from src.app import app


if __name__ == "__main__":
    app.config.from_object(Config)
    app.run(host=Config.HOST, port=Config.PORT, debug=True)
