import os

from app import create_app
from config import Config

app = create_app()

if __name__ == "__main__":
    if not os.path.exists(Config.DATABASE_PATH):
        raise SystemExit(
            "instance/toletearth.db not found — run `python migrations/seed_db.py` first."
        )
    app.run(debug=True)
