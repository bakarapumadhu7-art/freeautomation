import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    print(f"Starting Antigravity Automation Engine on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
