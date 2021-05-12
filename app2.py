from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///main.db"
db = SQLAlchemy(app)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url=db.Column(db.String(200), nullable=False)
    listing=db.Column(db.String(200), nullable=False)
    class_K_mean=db.Column(db.Integer, nullable=False)
    def __init__(self, url,listing,class_K_mean):
        self.url=url
        self.listing=listing
        self.class_K_mean=class_K_mean
    def __repr__(self):
        return  f"Object({self.id},'{self.url}','{self.listing}',{self.class_K_mean})"
