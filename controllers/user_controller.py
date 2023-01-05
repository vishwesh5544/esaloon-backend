import uuid
from datetime import datetime

from flask import current_app as app
from flask_restful import Resource, reqparse

from models.ApiResponseModel import ApiResponseModel
from models.User import User
from user_service.user_service import UserService
from utils.token_utils import TokenUtils


class UserController(Resource):

    def __init__(self):
        self.token_utils = TokenUtils()
        with app.app_context():
            self.user_service = UserService()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("fullname", type=str, required=True, help='Fullname cannot be empty.')
        parser.add_argument("phone", type=str, required=True, help='Phone number cannot be empty.')
        parser.add_argument("password", type=str, required=True, help='Password cannot be empty.')
        parser.add_argument("email", type=str, required=True, help='Email cannot be empty.')
        args = parser.parse_args()
        user = User(
            userid=uuid.uuid4().__str__(),
            fullname=args["fullname"],
            password=args["password"],
            email=args["email"],
            phone_number=args["phone"],
            creation_time=datetime.now().__str__()
        )

        return self.user_service.create_user_record(user), 201

    def get(self):
        pass


class UserLoginController(Resource):
    def __init__(self):
        self.token_utils = TokenUtils()
        with app.app_context():
            self.user_service = UserService()

    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument("Authorization", location='headers', type=str)
        parser.add_argument("email", required=True, help="Email cannot be empty.")
        parser.add_argument("password", required=True, help="Password cannot be empty.")
        args = parser.parse_args()
        # token = self.token_utils.get_token_from_header(args['Authorization'])
        # result = self.user_service.get_user_for_token(token)
        result = self.user_service.get_token_for_user(args['email'], args['password'])
        # result = self.user_service.get
        return ApiResponseModel(response_type="success", code=200, response=result, message="User authenticated and token received.").as_dict()
