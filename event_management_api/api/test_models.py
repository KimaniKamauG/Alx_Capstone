from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from events.models import Event, Category, EventRegistration
from django.contrib.auth import get_user_model

User = get_user_model()

class EventModelTests(TestCase):
    """Test suite for Event model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Conference',
            description='Tech conferences'
        )

    def test_create_valid_event(self):
        """Test creating event with valid data"""
        future_date = timezone.now() + timedelta(days=1)
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date_time=future_date,
            location='Test Location',
            organizer=self.user,
            capacity=100,
            category=self.category
        )
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.organizer, self.user)

    def test_past_date_validation(self):
        """Test validation prevents past dates"""
        past_date = timezone.now() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            Event.objects.create(
                title='Past Event',
                description='Test Description',
                date_time=past_date,
                location='Test Location',
                organizer=self.user,
                capacity=100
            )

    def test_event_registration(self):
        """Test event registration process"""
        future_date = timezone.now() + timedelta(days=1)
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date_time=future_date,
            location='Test Location',
            organizer=self.user,
            capacity=1
        )

        # Test successful registration
        registration = EventRegistration.objects.create(
            event=event,
            user=self.user
        )
        self.assertFalse(registration.is_waitlisted)

        # Test waitlist
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        registration2 = EventRegistration.objects.create(
            event=event,
            user=user2
        )
        self.assertTrue(registration2.is_waitlisted)