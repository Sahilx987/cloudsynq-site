import os
from dotenv import load_dotenv

load_dotenv()


MAIL_SERVER = os.getenv("MAIL_SERVER", "")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_TO = os.getenv("MAIL_TO", "sahila7mp@gmail.com")
MAIL_FROM = os.getenv("MAIL_USERNAME", "noreply@cloudsynq.shop")

FLASK_ENV = os.getenv("FLASK_ENV", "production")
DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
