"""Web Server Gateway Interface"""

from src.app import app

if __name__ == "__main__":
    app.run(debug=True)