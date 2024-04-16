from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#from dotenv import load_dotenv

from app import db 

# Define Task model
class Task(db.Model):
    __tablename__ = 'tasks'  # Specify the table name
    __table_args__ = {'schema': 'test'}  # Specify the schema name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)