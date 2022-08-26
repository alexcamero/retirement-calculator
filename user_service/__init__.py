import os, requests
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)

    @app.route('/users/<string:id>', methods = ["GET"])
    def get_user_info_by_id(id):
        url = os.getenv('USER_DATA_ENDPOINT') + id
        try:
            res = requests.get(url).json()
        except:
            res = {}
        return res

    return app