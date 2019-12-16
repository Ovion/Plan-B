import dotenv
import os

dotenv.load_dotenv()

KEY_ATLAS = os.getenv("KEY_ATLAS")
USER_ATLAS = 'ovi'
MONGO = "mongodb+srv://{}:{}@cluster0-ylnpw.mongodb.net/test"
