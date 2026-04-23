import os
from dotenv import load_dotenv
load_dotenv(override=True)
from app import create_app

app = create_app(os.environ.get("FLASK_ENV", "production"))

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False), use_reloader=False)
