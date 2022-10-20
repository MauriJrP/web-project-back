"""Web Server Gateway Interface"""

from src.app import App, db
from src.models import User, InvalidToken

app = App()

# @app.app.shell_context_processor
# def make_shell_context():

#     return {
#         'db': db,
#         'Users': User,
#         'InvalidToken': InvalidToken
#     }

# create all tables with app context
with app.app.app_context():
    print("Creating tables...")
    db.create_all()


if __name__ == "__main__":
    app.run()