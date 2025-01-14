import logging

from config import SLACK_APP_TOKEN
from modules.slack_apps.sample_app import app
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting Optibot...")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()


# アプリの起動
if __name__ == "__main__":
    main()
