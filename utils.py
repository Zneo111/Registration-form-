import random
import string
import re
from flask_mail import Message

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(mail, to_email, otp):
    msg = Message('Your OTP Code', recipients=[to_email])
    msg.body = f'Your OTP code is: {otp}'
    mail.send(msg)

def validate_email(email):
    # Simple regex for email validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_password(password):
    # At least 8 chars, 1 digit, 1 uppercase, 1 lowercase
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password))
