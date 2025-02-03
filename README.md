# Django User Authentication

This project is a simple user authentication system built with Django. It includes features for user registration, login, password reset, and a user dashboard.

## Features

- User Registration
- User Login
- Password Reset via Email
- User Dashboard
- Change Password

## Getting Started

### Prerequisites

- Python 3.x
- Django 5.x
- A Gmail account for sending emails (configured in settings)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install django
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/accounts/login/`.

## User Flow

### 1. User Registration

- Navigate to the signup page.
- Fill in the required fields (username, email, password).
- Click "Sign Up" to create a new account.

### 2. User Login

- Navigate to the login page.
- Enter your username and password.
- Click "SIGN IN" to log in.
- If the credentials are invalid, appropriate error messages will be displayed.

### 3. Password Reset

- If you forget your password, click on "Forgot Password?" on the login page.
- Enter your registered email address and click "Submit."
- Check your email for a password reset link.
- Click the link to set a new password.

### 4. User Dashboard

- After logging in, you will be redirected to the dashboard.
- The dashboard displays a welcome message and links to your profile, change password, and logout.

### 5. Change Password

- Click on "Change Password" in the dashboard.
- Enter your old password and the new password.
- Click "Change Password" to update your password.

## Email Configuration

To enable password reset functionality via email, configure your email settings.py
