🚀 Features

🔐 User Authentication (Register, Login, Logout)

💬 Send and receive private messages between users

📅 Message timestamps and ordering

👀 Read/Unread message tracking

🛠️ Admin panel for user and message management

🎨 Responsive UI (Django templates + Bootstrap/Tailwind)

⚡ Extendable for WebSockets/Channels (real-time chat)

🛠️ Tech Stack

Backend: Python, Django

Database: SQLite (default), PostgreSQL/MySQL (optional)

Frontend: Django Templates, Bootstrap/Tailwind CSS

Authentication: Django Auth (JWT/Allauth optional)

📂 Project Structure
messaging-app/
│── manage.py
│── requirements.txt
│── README.md
│
├── messaging_app/ # Main project settings
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── accounts/ # User authentication app
│ ├── models.py
│ ├── views.py
│ └── urls.py
│
└── messages/ # Messaging app
├── models.py
├── views.py
└── urls.py

⚙️ Installation & Setup

Clone the repository

git clone https://github.com/yourusername/messaging-app.git
cd messaging-app

Create a virtual environment & activate it

python -m venv venv
source venv/bin/activate # On Mac/Linux
venv\Scripts\activate # On Windows

Install dependencies

pip install -r requirements.txt

Apply migrations

python manage.py migrate

Create a superuser

python manage.py createsuperuser

Run the development server

python manage.py runserver

Open your browser at 👉 http://127.0.0.1:8000/

📸 Screenshots

(Add your own screenshots here for login, inbox, message view, etc.)

Login Page Inbox Chat Window

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
