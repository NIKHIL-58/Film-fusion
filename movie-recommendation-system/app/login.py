from app import app , mongo
from flask import request, jsonify, session 
from bson import ObjectId
from werkzeug.security import check_password_hash
import jwt


####################### LOGIN TO APP ##########################

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = mongo.db.users.find_one({'email': data['email']})


    if user and check_password_hash(user['password'], data['password']):
        userid = str(user.get("_id"))

        # Retrieve secret_key and algorithm from app.config
        secret_key = app.config['SECRET_KEY']
        algorithm = app.config['JWT_ALGORITHM']
        

        payload = {'userId': userid}
        token = jwt.encode(payload, secret_key, algorithm=algorithm)

        # Store token in session
        session['token'] = str(token)

        # Update the user document in MongoDB with the token
        mongo.db.users.update_one(
            {'_id': ObjectId(userid)},
            {'$set': {'token': token}}
        )

        return jsonify({
            "message": "Login successful",
            "user_id": str(user['_id']),
            "user": user['email'],
            "token": token
        }), 200
    else:
        return jsonify({
            "message": "Login Failed. Please check your email or password"
        }), 401
