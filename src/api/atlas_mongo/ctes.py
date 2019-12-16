import dotenv
import os

dotenv.load_dotenv()

ATLAS_KEY = os.getenv("KEY_ATLAS")
USER_ATLAS = 'ovi'
MONGO = "mongodb+srv://ovi:{}@cluster0-ylnpw.mongodb.net/test?retryWrites=true&w=majority"
