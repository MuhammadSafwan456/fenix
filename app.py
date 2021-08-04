from flask import Flask
from hashlib import sha256
from config.config import FLASK_KEY_SORTING, JWT_SECRET_KEY

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_SORT_KEYS"] = FLASK_KEY_SORTING
app.config["SECRET_KEY"] = sha256(JWT_SECRET_KEY.encode("ascii")).hexdigest()


from view.user import user_views
app.register_blueprint(user_views)
if __name__ == '__main__':
    app.run()
