from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from controllers.appointments_controller import AppointmentsController
from controllers.user_controller import UserController, UserLoginController

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(UserController, "/user")
api.add_resource(UserLoginController, "/user/login")
api.add_resource(AppointmentsController, "/appointments")


if __name__ == '__main__':
    app.run()
