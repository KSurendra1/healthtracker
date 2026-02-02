from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from apps.integrations.models import ExternalAccount
from apps.integrations.tasks import _sync_googlefit
from apps.tracker.models import Activity, HeartRate
from django.utils import timezone

class GoogleFitSyncTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testgfit', password='password')
        self.account = ExternalAccount.objects.create(
            user=self.user,
            provider='googlefit',
            access_token='fake_token',
            refresh_token='fake_refresh'
        )

    @patch('apps.integrations.googlefit.client.GoogleFitClient.__init__', return_value=None)
    @patch('apps.integrations.googlefit.client.GoogleFitClient.get_activities')
    @patch('apps.integrations.googlefit.client.GoogleFitClient.get_heart_rate')
    def test_sync_googlefit(self, mock_get_hr, mock_get_activities, mock_client_init):
        # Mock Activities Response
        mock_get_activities.return_value = {
            'bucket': [{
                'dataset': [
                    {
                        'dataSourceId': 'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps',
                        'point': [{'value': [{'intVal': 8500}]}]
                    },
                    {
                        'dataSourceId': 'derived:com.google.calories.expended:com.google.android.gms:merge_calories_expended',
                        'point': [{'value': [{'fpVal': 2100.5}]}]
                    }
                ]
            }]
        }

        # Mock Heart Rate Response
        mock_get_hr.return_value = {
            'bucket': [{
                'dataset': [
                    {
                        'dataSourceId': 'derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm',
                        'point': [{'value': [{'fpVal': 72.0}]}]
                    }
                ]
            }]
        }

        # Run sync
        _sync_googlefit(self.user, self.account)

        # Assert Activity created
        activity = Activity.objects.get(user=self.user, source='googlefit')
        self.assertEqual(activity.steps, 8500)
        self.assertEqual(activity.calories, 2100.5)

        # Assert Heart Rate created
        hr = HeartRate.objects.get(user=self.user)
        self.assertEqual(hr.bpm, 72)
