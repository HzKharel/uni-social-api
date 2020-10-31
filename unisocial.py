from flask import Flask
from flask_cors import CORS
from controllers.AuthController import Auth
from controllers.UserController import User
from controllers.PostsController import Post
from services.DatabaseService import DatabaseService

app = Flask(__name__)
CORS(app)
dbs = DatabaseService.get_instance()

app.register_blueprint(Auth, url_prefix='/auth')
app.register_blueprint(User, url_prefix='/user')
app.register_blueprint(Post, url_prefix='/posts')


@app.route('/')
def index():
    return 'Hello Web Tech'


if __name__ == '__main__':
    app.run(debug=True)


