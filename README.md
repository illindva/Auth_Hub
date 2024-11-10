# Auth_Hub

Auth_Hub is a secure and robust application designed to manage and store application credentials. Built using Flask and SQLAlchemy, this application ensures that all credentials are encrypted using AES-256 and hashed using pbkdf2 for maximum security.

![AuthHub Logo](https://github.com/illindva/Auth_Hub/blob/master/static/images/company_logo.png)

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

## Description

Auth_Hub provides a centralized solution to manage and store application credentials securely. It requires a valid user account to view and add credentials, ensuring that only authorized users can access sensitive information.

## Features

- **User Authentication:** Secure login and registration.
- **Role-based Access Control:** Differentiates between regular users and admin users.
- **Credential Encryption:** Uses AES-256 for encryption and pbkdf2 for password hashing.
- **Decryption on Demand:** Allows users to decrypt passwords for a limited time.
- **Approval Workflow:** Admins can approve or reject user accounts.

## Installation

To get started with Auth_Hub, follow these steps:

1. **Clone the Repo:**
    ```sh
    git clone https://github.com/illindva/Auth_Hub.git
    cd Auth_Hub
    ```

2. **Set Up Virtual Environment:**
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On Linux/Mac
    ```

3. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set Environment Variables:**
    Create a `.env` file in the root directory and add the necessary environment variables:
    ```plaintext
    FLASK_APP=app.py
    FLASK_ENV=development
    SECRET_KEY=your-secret-key
    SQLALCHEMY_DATABASE_URI=sqlite:///site.db
    APPLICATIONS=App1,App2,App3
    ```

5. **Initialize the Database:**
    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

6. **Run the Application:**
    ```sh
    flask run
    ```

## Usage

Detailed steps to use various features of Auth_Hub:

1. **Login:**
    - Navigate to `/login` and enter your credentials.
  
2. **Register:**
    - Visit `/register` to create a new account.

3. **Add Credentials:**
    - After logging in, go to `/form` to add new application credentials.

4. **View Credentials:**
    - Navigate to `/show-records` to view stored credentials.

5. **Decrypt Password:**
    - Click on the decrypt button next to the credential to decrypt the password for a limited time.

## Screenshots

### Home Page
![Home](https://github.com/illindva/Auth_Hub/blob/master/static/images/Home_Page.png)

### Login Page
![Login](https://github.com/illindva/Auth_Hub/blob/master/static/images/Login_Page.png)

### Add Credentials
![Add Credentials](https://github.com/illindva/Auth_Hub/blob/master/static/images/AddRecords_Page.png)

## Technologies

- **Framework:** Flask
- **Database:** SQLAlchemy
- **Frontend:** Bootstrap
- **Cryptography:** AES-256, pbkdf2

## Contributing

We welcome contributions! Please read `CONTRIBUTING.md` for details on the code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

© 2024 AuthHub by AskiTech Solutions Ltd. All rights reserved.
