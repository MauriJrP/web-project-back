"""Web Server Gateway Interface"""

from src.app import App, db
from src.models import User, InvalidToken

app = App()

# create all tables with app context
try:
    with app.app.app_context():
        print("Creating missing tables...")
        db.create_all()
        print("Tables created")

except Exception as e:
    print(f'Error: {e}')


if __name__ == "__main__":
    app.run()