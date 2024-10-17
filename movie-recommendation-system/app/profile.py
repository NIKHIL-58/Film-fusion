from app import app, mongo
from flask import request, jsonify, session
from werkzeug.utils import secure_filename 
import os
from bson import ObjectId
from .utils import verify_jwt_token
from app.config import Config

# @app.route('/api/user-profile', methods=['GET'])
# def user_profile():
#     token = session.get('token')
#     secret_key = app.config['SECRET_KEY']
#     algorithm = app.config['JWT_ALGORITHM']

#     try:
#         is_verified = verified_jwt_token(token. secret_key,algorithm)
#     except ValueError as e:
#         return jsonify({'message': str(e)}), 401
    
#     user_id = is_verified.get('userId')
#     if not user_id:
#         return jsonify({"message": "user not logged in"}), 401
    
#     user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
#     if user:
#         user_data = {
#             'name': user.get('name'),
#             'email': user.get('email'),
#             'profile_picture': user.get('profile_picture') or 'default-profile-image.png'
#         }
#         return jsonify(user_data), 200
#     else:
#         return jsonify({'message': 'user not found'}),404




@app.route('/api/user-profile', methods=['GET'])
def user_profile():
    token = session.get('token')
    secret_key = app.config['SECRET_KEY']
    algorithm = app.config['JWT_ALGORITHM']
    
    try:
        is_verified = verify_jwt_token(token, secret_key, algorithm)
    except ValueError as e:
        return jsonify({'message': str(e)}), 401
    
    user_id = is_verified.get('userId')
    if not user_id:
        return jsonify({'message': 'User not logged in'}), 401

    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        user_data = {
            'name': user.get('name'),
            'email': user.get('email'),
            'mobile': user.get('mobile'),
            'profile_picture': user.get('profile_picture') or 'default-profile-image.png'
        }
        return jsonify(user_data), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/update_profile', methods=['POST'])
def update_profile():
    token = session.get('token')
    secret_key = app.config['SECRET_KEY']
    algorithm = app.config['JWT_ALGORITHM']
    
    try:
        is_verified = verify_jwt_token(token, secret_key, algorithm)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    
    user_id = is_verified.get('userId')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    data = request.json
    updates = {}

    if 'userName' in data:
        updates['name'] = data['userName']
    if 'userEmail' in data:
        updates['email'] = data['userEmail']
    if 'userMobile' in data:
        updates['mobile'] = data['userMobile']

    if updates:
        result = mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': updates})
        if result.modified_count > 0:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'failed', 'message': 'No changes made'}), 400
    
    return jsonify({'status': 'failed', 'message': 'Invalid input'}), 400

@app.route('/upload_profile_picture', methods=['POST'])
def upload_profile_picture():
    token = session.get('token')
    secret_key = app.config['SECRET_KEY']
    algorithm = app.config['JWT_ALGORITHM']

    try:
        is_verified = verify_jwt_token(token, secret_key, algorithm)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    user_id = is_verified.get('userId')
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    # Check if a file is uploaded
    if 'profile_picture' not in request.files:
        return jsonify({'status': 'failed', 'message': 'No file part'}), 400

    file = request.files['profile_picture']

    # Ensure the file has a name
    if file.filename == '':
        return jsonify({'status': 'failed', 'message': 'No selected file'}), 400

    if file:
        # Secure the file name and save it to the upload folder
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Update the user's profile picture in the database
        result = mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'profile_picture': filename}}
        )

        if result.modified_count > 0:
            return jsonify({'status': 'success', 'profile_picture': filename}), 200
        else:
            return jsonify({'status': 'failed', 'message': 'Failed to update profile picture in the database'}), 500

    return jsonify({'status': 'failed', 'message': 'File upload failed'}), 400
