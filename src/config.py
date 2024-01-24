from dotenv import load_dotenv
import os

load_dotenv()

SECRET_AUTH = os.environ.get("SECRET_AUTH")
