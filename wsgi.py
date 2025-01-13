# for use with gunicorn only
# example: gunicorn --bind 0.0.0.0:2027 wsgi:app

from server import app

if __name__ == "__main__":
    app.run()