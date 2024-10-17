from app import app, mongo
from flask import request, jsonify, session
from bson import ObjectId
import jwt
from .utils import verify_jwt_token
from app.config import Config

secret_key = app.config['SECRET_KEY']
algorithm = app.config['JWT_ALGORITHM']


@app.route('/logout', methods=['POST'])
def logout():
    token = session.get('token')
    if token:
        try:
            decoded_token = jwt.decode(token, secret_key , algorithm)
            userId = decoded_token.get('userId')

            # Remove the token from the user's record in the database
            result = mongo.db.users.update_one(  {"_id": ObjectId(userId)},{"$set": {"token": ''}} )
            session.pop('token', None)
            return jsonify({'message': 'Logged out successfully'}), 200
        except jwt.ExpiredSignatureError:
            print("Token has expired, proceeding with logout")
        except jwt.InvalidTokenError:
            print("Invalid token, proceeding with logout")
        except Exception as e:
            print(f"Error while removing token from database: {e}")
    else:
        print("No token found in session")
    return jsonify({'message': 'Logged out successfully'}), 200
    

