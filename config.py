import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

API_KEY = os.getenv("STEAM_API_KEY")