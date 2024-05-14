# Library Book Management System

Welcome to the Library Book Management System! This system provides a platform for managing books, subscribers, and facilitating communication between administrators and subscribers.

## Features

### CRUD Operations
- **Administrator**: Perform CRUD operations (Create, Read, Update, Delete) on books and subscribers.
- **Subscribers**: View books and their own information.

### Issuing Functions
- **Administrator**: Issue books to subscribers.
- **Subscribers**: View issued books.

### Chat Functionality
- **Administrator and Subscribers**: Communicate with each other through a chat interface.
- **Share Queries**: Ask questions or share queries with the administrator.

### ReCAPTCHA and Email Verification
- **Registration**: Utilizes ReCAPTCHA to prevent bot registrations.
- **Email Verification**: Subscribers undergo email verification upon registration for added security.
- **Forget Password**: Subscribers can request a password reset via email.

### Logout
- **Both Administrators and Subscribers**: Logout functionality to securely end the session.

## Getting Started

### Prerequisites
- Ensure you have [Python](https://www.python.org/) installed on your system.
- Make sure you have [Git](https://git-scm.com/) installed for version control.

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your_username/library-book-management-system.git
    ```
2. Navigate to the project directory:
    ```bash
    cd library-book-management-system
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage
1. Start the application:
    ```bash
    python main.py
    ```
2. Access the application through your web browser by visiting [http://localhost:5000](http://localhost:5000).

## Contributing
Contributions are welcome! Please feel free to submit issues and pull requests.

## License
This project is licensed under the [MIT License](LICENSE).
