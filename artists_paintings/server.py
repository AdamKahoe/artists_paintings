from flask_app import app

from flask_app.controllers import controllers_users, controllers_paintings
from flask_app.models import models_user, models_painting

if __name__=="__main__":
    app.run(debug=True, port=5001)