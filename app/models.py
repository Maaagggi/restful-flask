from flask import jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import scrypt 

from app import db 

# Define Task model
class Task(db.Model):
    __tablename__ = 'tasks'  # Specify the table name
    __table_args__ = {'schema':'test'}  # Specify the schema name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Users(db.Model):
    __tablename = 'users'
    __table_args__ = {'schema':'test'}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
