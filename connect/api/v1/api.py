import datetime
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



    def log_in(self, username: str, password: str):
        user = db.session.query(models.User).filter_by(username=username).first()

        if not user:
            return {"message": "Invalid credentials"}, 401

        if not check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401


        if user.auth_token:
            return {"token": user.auth_token}, 200

        token = {"username": user.username, "email": user.email }
        encrypted = jwt.encode(token, current_app.config['SECRET_KEY'], algorithm="HS256")
        user.auth_token = encrypted
        db.session.commit()

        return {"token": encrypted}, 200
    
    def sign_up(self, username: str, email: str, password: str):
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

    def post(self, auth_type: str):
        print(request.headers, request.data, auth_type)

        if auth_type == "sign-in":
            args = self.log_in_parser.parse_args()
            username = args["username"]
            password = args["password"]

            return self.log_in(username, password)
        

        elif auth_type == "sign-up":
            args = self.sign_up_parser.parse_args()
            username = args["username"]
            email = args["email"]
            password = args["password"]

            return self.sign_up(username, email, password)
        

        else:
            return {"message": "Invalid auth_type"}, 400
        

def user_from_token(token: str):
    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    except Exception:
        return None

    return db.session.query(models.User).filter_by(username=decoded["username"]).first()


class EventResource(Resource):
    event_parser = reqparse.RequestParser()
    event_parser.add_argument("authorization", type=str, required=True)
    event_parser.add_argument("title", type=str, required=True)
    event_parser.add_argument("description", type=str, required=True)
    event_parser.add_argument("location", type=str, required=True)
    event_parser.add_argument("target_no_of_people", type=int, required=True)
    event_parser.add_argument("date", type=str, required=True)


    event_updator = reqparse.RequestParser()
    event_updator.add_argument("authorization", type=str, required=True)
    event_updator.add_argument("id", type=int, required=True)

    event_updator.add_argument("title", type=str, required=False)
    event_updator.add_argument("description", type=str, required=False)
    event_updator.add_argument("location", type=str, required=False)
    event_updator.add_argument("target_no_of_people", type=int, required=False)
    event_updator.add_argument("date", type=str, required=False)
    

    delete_parser = reqparse.RequestParser()
    delete_parser.add_argument("authorization", type=str, required=True)
    delete_parser.add_argument("id", type=int, required=True)


    def get(self, event_id: int):
        event = db.session.query(models.Event).filter_by(id=event_id).first()

        return (
            (event.to_dict(), 200)
            if event
            else ({"message": "Event not found"}, 404)
        )
    
    def post(self):
        args = self.event_parser.parse_args()


        title = args["title"]
        description = args["description"]
        location = args["location"]
        target_no_of_people = args["target_no_of_people"]
        date = args["date"]


        user = user_from_token(args["authorization"])

        if not user:
            return {"message": "Invalid token"}, 401
        

        date = datetime.datetime.fromisoformat(date)

        event = models.Event(title=title, description=description, location=location, target_no_of_people=target_no_of_people, date=date, user_id=user.id)
        db.session.add(event)
        db.session.commit()

        return {"message": "Event created", "id": event.id}, 201
    
    def put(self):
        args = self.event_updator.parse_args()

        user = user_from_token(args["authorization"])

        if not user:
            return {"message": "Invalid token"}, 401
        
        event = db.session.query(models.Event).filter_by(id=args["id"]).first()

        if not event:
            return {"message": "Event not found"}, 404
        
        if event.user_id != user.id:
            return {"message": "You are not the owner of this event"}, 403

        event.title = args["title"] or event.title
        event.description = args["description"] or event.description
        event.location = args["location"]or event.location
        event.target_no_of_people = args["target_no_of_people"] or event.target_no_of_people
        event.date = datetime.datetime.fromisoformat(args["date"]) or event.date

        db.session.commit()

        return {"message": "Event updated"}, 200
    

    def delete(self):
        args = self.delete_parser.parse_args()

        user = user_from_token(args["authorization"])

        if not user:
            return {"message": "Invalid token"}, 401
        
        event = db.session.query(models.ExternalEvent).filter_by(id=args["id"]).first()
        
        if event.user_id != user.id:
            return {"message": "You are not the owner of this event"}, 403

        if not event:
            return {"message": "Event not found"}, 404

        db.session.delete(event)
        db.session.commit()

        return {"message": "Event deleted"}, 200
    

# id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.String(1000), nullable=False)
#     link = db.Column(db.String(200), nullable=False)

class ExternalEventResource(Resource):
    event_parser = reqparse.RequestParser()
    event_parser.add_argument("authorization", type=str, required=True)
    event_parser.add_argument("title", type=str, required=True)
    event_parser.add_argument("description", type=str, required=True)
    event_parser.add_argument("link", type=str, required=True)
    event_parser.add_argument("date", type=str, required=True)


    event_updator = reqparse.RequestParser()
    event_updator.add_argument("authorization", type=str, required=True)
    event_updator.add_argument("id", type=int, required=True)

    event_updator.add_argument("title", type=str, required=False)
    event_updator.add_argument("description", type=str, required=False)
    event_updator.add_argument("link", type=str, required=False)
    event_updator.add_argument("date", type=str, required=False)
    

    delete_parser = reqparse.RequestParser()
    delete_parser.add_argument("authorization", type=str, required=True)
    delete_parser.add_argument("id", type=int, required=True)


    def get(self, event_id: int):
        event = db.session.query(models.ExternalEvent).filter_by(id=event_id).first()

        return (
            (event.to_dict(), 200)
            if event
            else ({"message": "Event not found"}, 404)
        )
    
    def post(self):
        args = self.event_parser.parse_args()

        title = args["title"]
        description = args["description"]
        link = args["link"]
        date = args["date"]


        user = user_from_token(args["authorization"])

        if not user:
            return {"message": "Invalid token"}, 401
        
        date = datetime.datetime.fromisoformat(date)
        
        event = models.ExternalEvent(title=title, description=description, link=link, date=date, user_id=user.id)
        db.session.add(event)
        db.session.commit()

        return {"message": "Event created", "id": event.id}, 201
    
    def put(self):
        args = self.event_updator.parse_args()
        user = user_from_token(args["authorization"])

        if not user:
            return {"message": "Invalid token"}, 401
        
        event = db.session.query(models.ExternalEvent).filter_by(id=args["id"]).first()

        if not event:
            return {"message": "Event not found"}, 404
        
        if event.user_id != user.id:
            return {"message": "You are not the owner of this event"}, 403

        event.title = args["title"] or event.title
        event.description = args["description"] or event.description
        event.link = args["link"]or event.link
        event.date = datetime.datetime.fromisoformat(args["date"]) or event.date

        db.session.commit()

        return {"message": "Event updated"}, 200
    

    def delete(self):
        args = self.delete_parser.parse_args()

        user = user_from_token(args["authorization"])

        if not user:
            return {"message": "Invalid token"}, 401
        
        event = db.session.query(models.ExternalEvent).filter_by(id=args["id"]).first()
        
        if event.user_id != user.id:
            return {"message": "You are not the owner of this event"}, 403

        if not event:
            return {"message": "Event not found"}, 404

        db.session.delete(event)
        db.session.commit()

        return {"message": "Event deleted"}, 200
    

class Events(Resource):
    def get(self, authorisation: str):

        user = user_from_token(authorisation)

        if not user:
            return {"message": "Invalid token"}, 401
        
        events = db.session.query(models.Event).filter_by(user_id=user.id).all()

        return (
            ({"events": [event.to_dict() for event in events]}, 200)
            if events
            else ({"message": "No events found"}, 404)
        )
    

class FutureEvents(Resource):
    def get(self):
        events = db.session.query(models.Event).filter(models.Event.date > datetime.datetime.now()).all()

        return (
            ({"events": [event.to_dict() for event in events]}, 200)
            if events
            else ({"message": "No events found"}, 404)
        )


class ExternalEvents(Resource):
    def get(self):
        events = db.session.query(models.ExternalEvent).filter(models.ExternalEvent.date > datetime.datetime.now()).all()

        return (
            ({"events": [event.to_dict() for event in events]}, 200)
            if events
            else ({"message": "No events found"}, 404)
        )
  
class DonationResource(Resource):
    def get(self, donation: int, authorisation: str):
       
        user = user_from_token(authorisation)
        
        if not user:
            return {"message": "Invalid token"}, 401
            
        donation = db.session.query(models.Donation).filter(models.Donation.id == donation).one()
        
        if not donation:
            return {"message": "Donation Not Found"}, 404
        
        if donation.user_id != user.id:
            return {"message": "Authentication Failure"}, 401
        
        return {"donation": donation.to_dict()}, 200
    
    
        
        

def set_resources(app: Flask):
    api = Api(app)
    api.add_resource(UserResource, "/api/v1/user/<string:auth_type>")
    api.add_resource(EventResource, "/api/v1/event", "/event/api/v1/<int:event_id>")
    api.add_resource(ExternalEventResource, "/api/v1/external_event", "/api/v1/external_event/<int:event_id>")
    api.add_resource(Events, "/api/v1/events/<string:authorisation>")
    api.add_resource(FutureEvents, "/api/v1/future_events")
    api.add_resource(ExternalEvents, "/api/v1/external_events")
    api.add_resource(DonationResource, "/api/v1/donation/", "/api/v1/donation/<int:donation>/<string:authorisation>" )
