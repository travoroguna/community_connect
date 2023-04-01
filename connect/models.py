from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask import current_app
from flask_migrate import Migrate
import datetime


db = current_app.extensions["sqlalchemy"]


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


    auth_token = db.Column(db.String(200), nullable=True)

    external_events = db.relationship("ExternalEvent", back_populates="user", lazy=True)
    events = db.relationship("Event", back_populates="user", lazy=True)
    donations = db.relationship("Donation", back_populates="user", lazy=True)


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    target_no_of_people = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="events")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "target_no_of_people": self.target_no_of_people,
            "date": self.date.isoformat() if self.date else None,
            "user_id": self.user_id,
        }


class Donation(db.Model):
    __tablename__ = "donations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    status = db.Column(db.String(100), nullable=False, default="pending")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="donations")
    
    def to_dict(self):
        return {
            "id":self.id,
            "event_id":self.event_id,
            "timestamp":self.timestamp,
            "status":self.status,
        }
        
class ExternalEvent(db.Model):
    __tablename__ = "external_events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="external_events")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "date": self.date.isoformat() if self.date else None,
            "user_id": self.user_id,
        }

