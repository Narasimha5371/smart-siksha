# Smart Sikhsha Backend

A Node.js backend for Smart Sikhsha login and signup system with MongoDB and email verification.

## Features

- User registration with email verification
- Secure login with password hashing
- MongoDB for data storage
- Email verification using Nodemailer
- CORS enabled for frontend integration

## Prerequisites

- Node.js (v14 or higher)
- MongoDB (local or cloud instance)
- Gmail account for email sending

## Installation

1. Clone the repository or download the files.

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables:
   - Copy `.env` file and update the values:
     ```
     MONGODB_URI=mongodb://localhost:27017/smart-sikhsha
     EMAIL_USER=your-email@gmail.com
     EMAIL_PASS=your-app-password
     PORT=5000
     ```

   **Note:** For Gmail, you need to generate an App Password:
   - Go to your Google Account settings
   - Enable 2-Factor Authentication
   - Generate an App Password for this application

4. Start MongoDB (if running locally):
   ```
   mongod
   ```

5. Start the server:
   ```
   npm start
   ```

   Or for development with auto-restart:
   ```
   npm run dev
   ```

The server will run on `http://localhost:5000`.

## API Endpoints

### POST /api/signup
Register a new user.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "language": "string",
  "class": "string"
}
```

### POST /api/verify
Verify user email with code.

**Request Body:**
```json
{
  "email": "string",
  "verificationCode": "string"
}
```

### POST /api/login
Login user.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

## Frontend Integration

The frontend files (`login.html` and `signup.html`) are updated to use these API endpoints. Make sure the backend is running before testing the frontend.

## Security Notes

- Passwords are hashed using bcryptjs
- Email verification prevents unauthorized account creation
- CORS is enabled for cross-origin requests from the frontend

## Technologies Used

- Node.js
- Express.js
- MongoDB with Mongoose
- Nodemailer for email
- bcryptjs for password hashing
- CORS for cross-origin requests
