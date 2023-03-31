from flask import Flask, current_app, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
import jwt
from connect import models
from werkzeug.security import check_password_hash, generate_password_hash


db = current_app.extensions["sqlalchemy"]


class UserResource(Resource):
    log_in_parser = reqparse.RequestParser()
    log_in_parser.add_argument("username", type=str, required=True)
    log_in_parser.add_argument("password", type=str, required=True)


    sign_up_parser = reqparse.RequestParser()
    sign_up_parser.add_argument("username", type=str, required=True)
    sign_up_parser.add_argument("email", type=str, required=True)
    sign_up_parser.add_argument("password", type=str, required=True)


    def post(self, auth_type: str):
        print(request.headers, request.data)

        if auth_type == "log_in":
            args = self.log_in_parser.parse_args()
            username = args["username"]
            password = args["password"]

            user = db.session.query(models.User).filter_by(username=username).first()

            if not user:
                return {"message": "Invalid credentials"}, 401
            
            if not check_password_hash(user.password, password):
                return {"message": "Invalid credentials"}, 401


            token = {"username": user.username, "email": user.email }
            encrypted = jwt.encode(token, current_app.config['SECRET_KEY'], algorithm="HS256")

            return {"token": encrypted}, 200
        

        elif auth_type == "sign_up":
            args = self.sign_up_parser.parse_args()
            username = args["username"]
            email = args["email"]
            password = args["password"]

            user = db.session.query(models.User).filter_by(username=username).first()

            if user:
                return {"message": "Username already exists"}, 400
            

            e = db.session.query(models.User).filter_by(email=email).first()

            if e:
                return {"message": "Email already exists"}, 400
            
            password = generate_password_hash(password)

            user = models.User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()


            return {"message": "User created"}, 201
        

        else:
            return {"message": "Invalid auth_type"}, 400


def set_resources(app: Flask):
    api = Api(app)
    api.add_resource(UserResource, "/user/api/v1/<string:auth_type>")