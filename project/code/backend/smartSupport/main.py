import os
from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore

from flask_cors import CORS
from flask_babel import Babel


from app.config.config import LocalConfig
from app.config.flask_security import ExtendedRegisterForm
from app.data.db import db
from app.data.models import User, Role


app = None
api = None
cache = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', 'dev') == 'production':
        raise Exception("Please Config production env and update this section")
    else:
        app.config.from_object(LocalConfig)
    app.app_context().push()    

    db.init_app(app)
    app.app_context().push()

    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)    
    app.security = Security(app, user_datastore, register_form=ExtendedRegisterForm) 

    app.app_context().push()

    return app, api


app, api = create_app()
CORS(app)
babel = Babel(app)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)