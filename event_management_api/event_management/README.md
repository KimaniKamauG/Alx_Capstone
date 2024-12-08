EVENT MANAGEMENT API:
PROJECT DESCRIPTION:

The Event Management API is a Django-based RESTful API that allows users to manage events through a web interface or programmatically via API calls. The API supports the creation, retrieval, updating and deletion (CRUD operations) of events, as well as listing upcoming events. The API is designed to manage event data, provide a way to view scheduled events, and interact with the event management system.

This API will be ideal for use cases where users need to organize and track events, and provide a public API for interacting with event-related data.

CORE FEATURES AND FUNCTIONALITY:

Create Events:
Authenticated users can create events by providing details such as event name, description, date, and the creator’s user information.
View Event Details:
Any user can view the details of a specific event, including the name, description, date, and the user who created the event.
Update Events:
Authenticated users can edit and update the details of the events they have created.
Delete Events:
Authenticated users can delete events they have created.
View Upcoming Events:
Any user can retrieve a list of upcoming events, sorted by their date.
User Authentication:
The API requires user authentication for creating, updating, and deleting events. Only the user who created an event can edit it or delete it. 



API ENDPOINTS TO IMPLEMENT:
Create Event (POST /api/events/): Allows authenticated users to create new events.
View Event(GET /api/events): Retrieve the details of a specific event by its ID.
Update Event(PUT /api/events/): Allows authenticated users to update event details.
Delete Event(DELETE /api/events/<id>/delete/): Allows authenticated users to delete an event they created.
View Upcoming Events(GET /api/events/upcoming/): Retrieves a list of upcoming events sorted by date.


TOOLS AND LIBRARIES TO USE:
Django -  a Python-based web framework used for creating the API and handling the backend logic
Django REST Framework (DRF) - a powerful toolkit for building web APIs in Django. Used to handle the serialization, viewsets, and API endpoints.
SQLite/PostreSQL Database - The former for local development and the latter for production development.
User Authentication - Utilizes Django’s built-in user authentication system for handling login, user management, and permissions.
Heroku - Platform-as-a-service (PaaS) for hosting and deploying the Django API.
Postman - For testing and making API requests, suitable for manual testing.


FUTURE ENHANCEMENTS:
Tagging Events - allow users to tag events to categorize them.
Search functionality - add search capabilities based on event name or description.
Event notifications - add email or push notifications to users for event updates
