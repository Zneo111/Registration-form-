from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from models import db, User
from utils import generate_otp, send_otp_email, validate_email, validate_password
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

db.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not (email and username and password):
        return jsonify({'error': 'Missing fields'}), 400
    if not validate_email(email):
        return jsonify({'error': 'Invalid email'}), 400
    if not validate_password(password):
        return jsonify({'error': 'Password too weak'}), 400
    if User.query.filter((User.email == email) | (User.username == username)).first():
        return jsonify({'error': 'User already exists'}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    user = User(username=username, email=email, password=hashed_pw, otp=otp, otp_expiry=otp_expiry)
    db.session.add(user)
    db.session.commit()
    send_otp_email(mail, email, otp)
    return jsonify({'message': 'Registered. Please verify OTP sent to your email.'}), 201

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    user = User.query.filter_by(email=email).first()
    if not user or not otp:
        return jsonify({'error': 'Invalid request'}), 400
    if user.otp != otp or datetime.utcnow() > user.otp_expiry:
        return jsonify({'error': 'Invalid or expired OTP'}), 400
    user.is_verified = True
    user.otp = None
    user.otp_expiry = None
    db.session.commit()
    return jsonify({'message': 'Email verified successfully.'}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    if not user.is_verified:
        return jsonify({'error': 'Email not verified'}), 403
    # Generate OTP for 2FA
    otp = generate_otp()
    user.otp = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()
    send_otp_email(mail, email, otp)
    return jsonify({'message': 'OTP sent to email for 2FA'}), 200

@app.route('/login-2fa', methods=['POST'])
def login_2fa():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    user = User.query.filter_by(email=email).first()
    if not user or not otp:
        return jsonify({'error': 'Invalid request'}), 400
    if user.otp != otp or datetime.utcnow() > user.otp_expiry:
        return jsonify({'error': 'Invalid or expired OTP'}), 400
    user.otp = None
    user.otp_expiry = None
    db.session.commit()
    return jsonify({'message': 'Login successful'}), 200

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    otp = generate_otp()
    user.otp = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()
    send_otp_email(mail, email, otp)
    return jsonify({'message': 'OTP sent to email for password reset'}), 200

@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    new_password = data.get('new_password')
    user = User.query.filter_by(email=email).first()
    if not user or not otp or not new_password:
        return jsonify({'error': 'Invalid request'}), 400
    if user.otp != otp or datetime.utcnow() > user.otp_expiry:
        return jsonify({'error': 'Invalid or expired OTP'}), 400
    if not validate_password(new_password):
        return jsonify({'error': 'Password too weak'}), 400
    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.otp = None
    user.otp_expiry = None
    db.session.commit()
    return jsonify({'message': 'Password reset successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)
