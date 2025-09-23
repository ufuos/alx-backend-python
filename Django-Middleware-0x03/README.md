Django-Middleware-0x03 🚀
Features
🔐 Authentication & Messaging

User Authentication (Register, Login, Logout)

Send and receive private messages between users

Message timestamps and ordering

Read/Unread message tracking

Admin panel for user and message management

Responsive UI (Django templates + Bootstrap/Tailwind)

Extendable for WebSockets/Channels (real-time chat)

🧩 Middleware Features

RolePermissionMiddleware → Enforces role-based access (e.g., only Admins/Moderators can perform restricted actions).

RequestLoggingMiddleware → Logs every request with user, path, method, and timestamp.

ExecutionTimeMiddleware → Measures and logs request processing time for performance monitoring.

RateLimitMiddleware → Throttles excessive requests per user/IP to prevent abuse (basic rate limiting).

CustomHeaderMiddleware → Adds security and project-specific headers to all HTTP responses.

MaintenanceModeMiddleware → Blocks non-admin users when the site is in maintenance mode.

ExceptionHandlingMiddleware → Catches unhandled errors and returns clean, JSON-friendly error responses.

🛠️ Tech Stack

Backend: Python, Django

Database: SQLite (default), PostgreSQL/MySQL (optional)

Frontend: Django Templates, Bootstrap/Tailwind CSS

Authentication: Django Auth (JWT/Allauth optional)

⚙️ Installation & Setup

Clone the repository:

git clone https://github.com/yourusername/messaging-app.git
cd messaging-app

Create a virtual environment & activate it:

python -m venv venv
source venv/bin/activate # On Mac/Linux
venv\Scripts\activate # On Windows

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Create a superuser:

python manage.py createsuperuser

Run the development server:

python manage.py runserver

Open your browser at 👉 http://127.0.0.1:8000/

📸 Screenshots

(Add your own screenshots here for login, inbox, message view, etc.)

Login Page

Inbox

Chat Window

🧪 Running Tests
python manage.py test

🚀 Deployment

Can be deployed to Heroku, Render, Railway, or DigitalOcean.

Make sure to set up:

ALLOWED_HOSTS in settings.py

Environment variables (.env) for database and secret key

📜 License

This project is licensed under the MIT License – feel free to use and modify.

🤝 Contributing

Contributions are welcome!

Fork the repo

Create a new branch (feature-xyz)

Commit changes

Submit a Pull Request
