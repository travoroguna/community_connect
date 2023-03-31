from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

 


class UserResource(Resource):
    log_in_parser = reqparse.RequestParser()
    log_in_parser.add_argument("username", type=str, required=True)
    log_in_parser.add_argument("password", type=str, required=True)


    sign_up_parser = reqparse.RequestParser()
    sign_up_parser.add_argument("username", type=str, required=True)
    sign_up_parser.add_argument("email", type=str, required=True)
    sign_up_parser.add_argument("password", type=str, required=True)


    def get(self, auth_type: str):
        if auth_type == "log_in":
            args = self.log_in_parser.parse_args()
            username = args["username"]
            password = args["password"]
            return {"username": username, "password": password}
        elif auth_type == "sign_up":
            args = self.sign_up_parser.parse_args()
            username = args["username"]
            email = args["email"]
            password = args["password"]
            return {"username": username, "email": email, "password": password}
        else:
            return {"message": "Invalid auth_type"}, 400

def set_resources(api: Api):
    api.add_resource(UserResource, "/user/<string:auth_type>")