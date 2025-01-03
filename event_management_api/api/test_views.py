from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from events.models import Event, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class EventViewSetTests(APITestCase):
    """Test suite for EventViewSet"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(
            name='Conference',
            description='Tech conferences'
        )

    def test_create_event(self):
        """Test event creation"""
        url = reverse('event-list')
        future_date = (timezone.now() + timedelta(days=1)).isoformat()
        data = {
            'title': 'New Test Event',
            'description': 'Test Description',
            'date_time': future_date,
            'location': 'Test Location',
            'capacity': 100,
            'category': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().title, 'New Test Event')

    def test_register_for_event(self):
        """Test event registration"""
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date_time=timezone.now() + timedelta(days=1),
            location='Test Location',
            organizer=self.user,
            capacity=1
        )
        url = reverse('event-register', kwargs={'pk': event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['waitlisted'])

 