# Flask Registration API

A Flask-based registration system with password hashing, email verification, and OTP functionality.

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Registration-form--1
```

2. Create and activate virtual environment using pipenv:
```bash
pipenv install
pipenv shell
```

3. Install the required dependencies:
```bash
pipenv install flask flask-sqlalchemy flask-bcrypt flask-mail email-validator
```

4. Initialize the database:
```python
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

## Configuration

Update the following configurations in `app.py`:

1. Set your secret key:
```python
app.config['SECRET_KEY'] = 'your-secret-key'
```

2. Configure email settings:
```python
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

## Testing the API

You can test the API endpoints using curl or Postman:

### 1. Register a new user

```bash
curl -X POST http://localhost:5000/register \
-H "Content-Type: application/json" \
-d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
}'
```

Expected response:
```json
{
    "message": "Registration successful. Please verify OTP."
}
```

### 2. Verify OTP

```bash
curl -X POST http://localhost:5000/verify-otp \
-H "Content-Type: application/json" \
-d '{
    "email": "test@example.com",
    "otp": "123456"
}'
```

Expected response:
```json
{
    "message": "Email verified successfully"
}
```

## API Endpoints

1. `/register` (POST)
   - Registers a new user
   - Sends OTP to email
   - Required fields: username, email, password

2. `/verify-otp` (POST)
   - Verifies the OTP sent to email
   - Required fields: email, otp

## Error Handling

The API returns appropriate error messages with status codes:

- 400: Bad Request (Missing fields, Invalid data)
- 404: Not Found (User not found)
- 201: Created (Successful registration)
- 200: OK (Successful verification)

## Running the Application

```bash
pipenv run python app.py
```

The server will start at `http://localhost:5000`
