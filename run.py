import os
from app import create_app

# Default to development if not specified
env_name = os.getenv("FLASK_ENV", "development")
app = create_app(env_name)

if __name__ == '__main__':
    app.run(debug=(env_name == "development"))
