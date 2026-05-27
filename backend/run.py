import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3001))
    app.run(debug=True, port=port, host="0.0.0.0")