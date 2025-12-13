from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.models.plannedEvent import PlannedEvent
from app.models.profile import Profile
# Import your factories
from app.factory import ProfileFactory, PlannedEventFactory 

User = get_user_model()

class PlannedEventCRUDTests(APITestCase):
    
    def setUp(self):
        # create User (profile should be auto)
        self.user = User.objects.create_user(username='testuser', password='password')
        # ensure profile exists
        if not hasattr(self.user, 'profile'):
            self.profile = Profile.objects.create(user=self.user)
        else:
            self.profile = self.user.profile

        
        self.client.force_authenticate(user=self.user)

        # 3. Define the base URL (basename in urls.py was 'plannedevent')
        # This usually resolves to /api/events/
        self.list_url = reverse('plannedevent-list')

    def test_create_planned_event(self):
        """
        Test that a logged-in user can create an event and the creator is assigned automatically.
        """
        data = {
            "title": "Meeting with Client",
            "description": "Discuss project roadmap",
            "date": "2024-12-25",
            "start_time": "14:00:00",
            "duration": "01:00:00"
        }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlannedEvent.objects.count(), 1)
        
        # Verify the creator was set correctly to the logged in user
        event = PlannedEvent.objects.get()
        self.assertEqual(event.creator, self.profile)
        self.assertEqual(event.title, "Meeting with Client")

    def test_list_events_shows_only_own_data(self):
        """
         User A should not see User B's events.
        """
        #arrange
        my_event = PlannedEventFactory(creator=self.profile)

        other_user = User.objects.create_user(username='other', password='pw')
        other_profile = Profile.objects.create(user=other_user)
        other_event = PlannedEventFactory(creator=other_profile)

        #act
        response = self.client.get(self.list_url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], my_event.id)

    def test_update_event(self):
        event = PlannedEventFactory(creator=self.profile)
        detail_url = reverse('plannedevent-detail', args=[event.id])
        
        updated_data = {
            "title": "Updated Title",
            "date": event.date,
            "start_time": event.start_time,
            "duration": event.duration
        }

        response = self.client.put(detail_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        self.assertEqual(event.title, "Updated Title")

    def test_delete_event(self):

        event = PlannedEventFactory(creator=self.profile)
        detail_url = reverse('plannedevent-detail', args=[event.id])

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PlannedEvent.objects.count(), 0)

    def test_cannot_access_other_users_event(self):
        """
        User A shouldn't GET/UPDATE/DELETE User B's event by ID.
        """
        other_user = User.objects.create_user(username='other', password='pw')
        other_profile = Profile.objects.create(user=other_user)
        other_event = PlannedEventFactory(creator=other_profile)

        detail_url = reverse('plannedevent-detail', args=[other_event.id])
        
        response = self.client.get(detail_url)

        # shoudl return 404 instead of 403 to avoid info leak
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 
       