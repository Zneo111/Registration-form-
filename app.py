from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password', 'username']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Generate OTP
    otp = ''.join(random.choices(string.digits, k=6))
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    
    # Hash password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        otp=otp,
        otp_expiry=otp_expiry,
        is_verified=False
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # Send OTP email
    send_otp_email(data['email'], otp)
    
    return jsonify({'message': 'Registration successful. Please verify OTP.'}), 201

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'otp']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user.otp != data['otp']:
        return jsonify({'error': 'Invalid OTP'}), 400
    
    if datetime.utcnow() > user.otp_expiry:
        return jsonify({'error': 'OTP expired'}), 400
    
    user.is_verified = True
    db.session.commit()
    
    return jsonify({'message': 'Email verified successfully'}), 200

def send_otp_email(email, otp):
    msg = Message('Email Verification OTP',
                sender='your-email@gmail.com',
                recipients=[email])
    msg.body = f'Your OTP for email verification is: {otp}'
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
