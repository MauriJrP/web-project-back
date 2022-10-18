"""Web Server Gateway Interface"""

from src.app import App

app = App()

if __name__ == "__main__":
    app.run()