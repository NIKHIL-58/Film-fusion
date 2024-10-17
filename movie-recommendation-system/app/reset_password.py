from app import app, mongo
from flask import Flask ,request, jsonify, render_template, redirect, url_for
import os
import random
from .utils import send_otp_email
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash


otp_storage = {}

@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    user = mongo.db.users.find_one({'email': email})
    if user:
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp

        send_otp_email(email, otp)
        print(f'OTP:{otp}')

        # Send user to /verify-otp with email as a query parameter
        return jsonify({'message': 'Email found, OTP sent to email', 'next_step': f'/verify-otp?email={email}'}), 200
    else:
        return jsonify({'message': 'Email not found'}), 404


@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    user_otp = data.get('otp')

    # Check if the email exists in the database
    user = mongo.db.users.find_one({"email": email})
    
    if not user:
        return jsonify({"message": "Email not found!"}), 404

    # Check if the OTP matches and is of correct length
    if otp_storage.get(email) == user_otp and len(user_otp) == 6:
        # OTP verified successfully, redirect to reset-password page
        return jsonify({"message": "OTP verified successfully!", "next_step": f"/reset-password?email={email}"}), 200
    else:
        return jsonify({"message": "Invalid OTP!"}), 400


from flask import jsonify, request
from werkzeug.security import generate_password_hash

@app.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.json
        email = data.get('email')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Check if the email exists in the database
        user = mongo.db.users.find_one({"email": email})
        
        if not user:
            return jsonify({"message": "Email not found!"}), 404

        # Ensure both new_password and confirm_password are present
        if not email or not new_password or not confirm_password:
            return jsonify({"message": "Email, New password, and Confirm password are required!"}), 400

        # Ensure passwords match
        if new_password != confirm_password:
            return jsonify({"message": "Passwords do not match!"}), 400

        # Hash the new password
        hashed_password = generate_password_hash(new_password)

        # Update the user's password in the database
        result = mongo.db.users.update_one(
            {'email': email},
            {'$set': {'password': hashed_password}}
        )

        if result.matched_count > 0:
            return jsonify({"message": "Password reset successfully!"}), 200
        else:
            return jsonify({"message": "Email not found!"}), 404

    except Exception as e:
        # Log the error
        print(f"Error resetting password: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
