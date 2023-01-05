import uuid

import mysql.connector
from flask_bcrypt import Bcrypt

from database.db import Db
from models.ApiResponseModel import ApiResponseModel
from models.Token import Token
from models.User import User
from models.UserAndToken import UserAndToken
import jwt

from models.UserAndTokenSingle import UserAndTokenSingle


class UserService:
    db = mysql.connector
    connection = mysql.connector.connection
    bcrypt = Bcrypt()

    def __init__(self):
        self.db = Db()
        self.jwt = jwt

    def create_user_record(self, user: User) -> ApiResponseModel:
        self.bcrypt = Bcrypt()
        cursor = self.db.cursor
        pwd_hash = self.bcrypt.generate_password_hash(user.password)
        setattr(user, 'password', pwd_hash)

        try:
            # create user and token record
            token = Token(tokenid=uuid.uuid4().__str__(), token=self.create_token_for_user(user.email), email=user.email)
            user_and_token = UserAndToken(user=user, tokens_list=[token])

            # insert user data
            user_query = "INSERT INTO users(user_id, fullname, phone, email, password, creation_date) VALUES(%s,%s,%s,%s,%s,%s)"
            user_val = (user_and_token.user.userid, user_and_token.user.fullname, user_and_token.user.phone_numer,
                        user_and_token.user.email,
                        user_and_token.user.password, user_and_token.user.creation_date)

            # insert insert token for user
            token_query = "INSERT INTO tokens(token, email) VALUES(%s,%s)"
            token_val = (user_and_token.tokens_list[0].token, user_and_token.user.email)

            # print(json.dumps(self.user_records, indent=4, cls=EnhancedJSONEncoder))

            cursor.execute(user_query, user_val)
            cursor.execute(token_query, token_val)
            self.db.connection.commit()

            user_created = self.get_user_record_by_email(email=user.email)
            print(f'*** User Created: ${user_created}')
            return ApiResponseModel(code=200, message="user created successfully", response_type="success", response=user_created).as_dict()

        except mysql.connector.Error as e:
            print(e)

        finally:
            cursor.close()

    def get_user_record_by_email(self, email: str):
        cursor = self.db.cursor
        query = "SELECT user_id,  fullname, email FROM users WHERE email = %s"
        val = [email]
        cursor.execute(query, val)
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            print(f'*** User Retrieved: ${result}')
            return result

    def create_token_for_user(self, email: str) -> str:
        payload = {
            "iss": "http://localhost:5000",
            "sub": "esaloon-access",
            "user": email,
        }

        key = "vish's-ultra-strong-key-with-" + email
        token = self.jwt.encode(payload, key, algorithm="HS256")
        print('***** token: ', token)
        return token

    def get_token_for_user(self, email: str, password: str):
        cursor = self.db.cursor
        query = "SELECT * FROM users INNER JOIN tokens WHERE users.email = %s AND users.email = tokens.email"
        val = [email]
        cursor.execute(query, val)
        user_details = cursor.fetchone()
        result = self.bcrypt.check_password_hash(user_details['password'], password)
        print(user_details)
        if result is True:
            return UserAndTokenSingle(email=user_details['email'], token=user_details['token'])

    def delete_user_record(self, email: str) -> int:

        cursor = self.db.cursor
        query = "DELETE FROM users WHERE email = %s"
        val = [email]
        cursor.execute(query, val)
        self.db.connection.commit()
        return cursor.rowcount

    def delete_user_token(self, token: str):
        email_by_token = self.get_user_for_token(token=token)['email']
        deleted_rows = self.delete_user_record(email=email_by_token)
        if deleted_rows > 0:
            cursor = self.db.cursor
            query = "DELETE FROM tokens WHERE email = %s"
            val = [email_by_token]

            try:
                cursor.execute(query, val)
                self.db.connection.commit()

                if cursor.rowcount > 0:
                    print(f'User ${email_by_token} deleted')
            except mysql.connector.Error as e:
                print(e)
            finally:
                cursor.close()
        else:
            print("User deletion failed")

    def get_user_for_token(self, token: str):
        cursor = self.db.cursor
        query = "SELECT * FROM tokens WHERE token = %s"
        val = [token]
        cursor.execute(query, val)
        self.db.connection.commit()
        return cursor.fetchone()
