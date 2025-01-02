THIS DOCUMENTATION CONTAINS ALL THE IMPORTANT INFORMATION CONCERNING THIS PROJECT.
IT INCLUDES THE FEATURES OF THE API AND HOW TO RUN IT ON YOUR LOCAL MACHINE.



# Event Management API

A Django REST Framework-based API for managing events, registrations, and user interactions.

## Features

- User Authentication with JWT
- Event Management (CRUD operations)
- Event Registration System
- Email Notifications
- Google Calendar Integration
- API Documentation with Swagger/ReDoc
- Comprehensive Test Suite

## Tech Stack

- Django 3.2+
- Django REST Framework
- Simple JWT for authentication
- Google Calendar API
- Swagger/ReDoc for API documentation
- SQLite (development) / PostgreSQL (production)

## Installation

1. Clone the repository:

bash
git clone https://github.com/KimaniKamauG/ALX_Capstone.git
cd event_management_api


2. Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows


3. Install dependencies:

bash
pip install -r requirements.txt



4. Create .env file:

DJANGO_SECRET_KEY=
DJANGO_DEBUG=
EMAIL_HOST_USER=your-
EMAIL_HOST_PASSWORD=
GOOGLE_CLIENT_ID=
GOOGLE_PROJECT_ID=
GOOGLE_CLIENT_SECRET=



5. Run migrations:

bash
python manage.py makemigrations
python manage.py migrate


6. Create superuser:

bash
python manage.py createsuperuser


7. Run the development server:

bash
python manage.py runserver


## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/` - List users
- `POST /api/users/` - Create user
- `GET /api/users/{id}/` - Retrieve user
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Events
- `GET /api/events/` - List events
- `POST /api/events/` - Create event
- `GET /api/events/{id}/` - Retrieve event
- `PUT /api/events/{id}/` - Update event
- `DELETE /api/events/{id}/` - Delete event
- `POST /api/events/{id}/register/` - Register for event
- `POST /api/events/{id}/unregister/` - Unregister from event
- `POST /api/events/{id}/add_to_calendar/` - Add to Google Calendar

### Documentation
- `/swagger/` - Swagger UI
- `/redoc/` - ReDoc UI

## Testing

Run tests with:

bash
python manage.py test --settings=event_management_api.test_settings



## Deployment

### PythonAnywhere Setup

1. Create a PythonAnywhere account

2. Upload code:


bash
git clone https://github.com/KimaniKamauG/event_management_api.git


3. Create virtual environment:

bash
mkvirtualenv --python=/usr/bin/python3.8 event_env
pip install -r requirements.txt


4. Configure web app:
- Domain name
- Virtual environment path
- Static files
- WSGI configuration

5. Set environment variables in PythonAnywhere dashboard

6. Collect static files:

bash
python manage.py collectstatic


## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.