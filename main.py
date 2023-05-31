import src.routes  # NOQA
from config import Config, TestConfig
from src.app import create_app


if __name__ == "__main__":
    create_app(Config).run(host=Config.HOST, port=Config.PORT, debug=True)
