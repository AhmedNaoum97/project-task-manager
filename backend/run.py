import os
from app import create_app, db
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_ENV") == "development"
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)