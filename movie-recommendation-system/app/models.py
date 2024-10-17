from flask_pymongo import PyMongo

# Initialize PyMongo instance
mongo = PyMongo()

def init_app(app):
    # Initialize PyMongo with the Flask app
    mongo.init_app(app)
