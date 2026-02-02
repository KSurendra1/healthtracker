from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from apps.integrations.models import ExternalAccount
from apps.integrations.tasks import _sync_fitbit
from apps.tracker.models import Activity, HeartRate

class FitbitSyncTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.account = ExternalAccount.objects.create(
            user=self.user,
            provider='fitbit',
            access_token='fake_token',
            provider_user_id='fake_user_id'
        )

    @patch('apps.integrations.fitbit.client.FitbitClient.get_activities')
    @patch('apps.integrations.fitbit.client.FitbitClient.get_heart_rate')
    def test_sync_activites_and_hr(self, mock_get_hr, mock_get_activities):
        # Mock API responses
        mock_get_activities.return_value = {
            'summary': {
                'steps': 5000,
                'caloriesOut': 2000
            }
        }
        mock_get_hr.return_value = {
            'activities-heart': [
                {
                    'value': {'restingHeartRate': 65}
                }
            ]
        }

        # Run sync
        _sync_fitbit(self.user, self.account)

        # Assert Activity created
        activity = Activity.objects.get(user=self.user, source='fitbit')
        self.assertEqual(activity.steps, 5000)
        self.assertEqual(activity.calories, 2000)

        # Assert Heart Rate created
        hr = HeartRate.objects.get(user=self.user)
        self.assertEqual(hr.bpm, 65)
