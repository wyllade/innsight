import os
from app import create_app
from app.seed import seed_db

app = create_app()
seed_db(app)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3001))
    app.run(debug=True, use_reloader=False, port=port, host="0.0.0.0")