# Flask Registration Backend

## How to Run

1. **Install pipenv if you don't have it:**
   ```bash
   pip install pipenv
   ```

2. **Install dependencies:**
   ```bash
   pipenv install
   ```

3. **Set environment variables for email and secret key:**
   ```bash
   export MAIL_USERNAME='your-gmail@gmail.com'
   export MAIL_PASSWORD='your-app-password'
   export SECRET_KEY='your-secret-key'
   ```

4. **Activate the virtual environment:**
   ```bash
   pipenv shell
   ```

5. **Run the app using Flask CLI:**
   ```bash
   flask run
   ```
   The API will be available at `http://localhost:5000`

## Features

- User registration with email verification (OTP)
- Password hashing and salting
- 2FA (OTP) on login
- Forgot password and password reset with OTP
- Input validation

## Setup

1. **Clone the repo and enter the directory**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables for email**
   ```bash
   export MAIL_USERNAME='your-gmail@gmail.com'
   export MAIL_PASSWORD='your-app-password'
   export SECRET_KEY='your-secret-key'
   ```
   - Use an [App Password](https://support.google.com/accounts/answer/185833) if you have 2FA enabled on Gmail.

4. **Run the app**
   ```bash
   python app.py
   ```

## API Endpoints

### Register
`POST /register`
```json
{
  "username": "yourname",
  "email": "your@email.com",
  "password": "StrongPass123"
}
```

### Verify OTP (after registration)
`POST /verify-otp`
```json
{
  "email": "your@email.com",
  "otp": "123456"
}
```

### Login (step 1)
`POST /login`
```json
{
  "email": "your@email.com",
  "password": "StrongPass123"
}
```
- Returns: OTP sent to email

### Login 2FA (step 2)
`POST /login-2fa`
```json
{
  "email": "your@email.com",
  "otp": "123456"
}
```

### Forgot Password
`POST /forgot-password`
```json
{
  "email": "your@email.com"
}
```

### Reset Password
`POST /reset-password`
```json
{
  "email": "your@email.com",
  "otp": "123456",
  "new_password": "NewStrongPass123"
}
```

## Testing

- Use [Postman](https://www.postman.com/) or `curl` to test endpoints.
- Check your email for OTPs.

## Notes

- Passwords must be at least 8 characters, with uppercase, lowercase, and a digit.
- OTPs expire after 10 minutes.
- All responses are JSON.

---

# Registration Form

## Installation

To install the dependencies, run:

```bash
npm install
```

or, if you use yarn:

```bash
yarn install
```

## Test Run

To test run the files, use:

```bash
npm start
```

or, if you use yarn:

```bash
yarn start
```
