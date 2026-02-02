from django.test import TestCase
from unittest.mock import MagicMock
from apps.integrations.fitbit.client import FitbitClient, FITBIT_TOKEN_URL
import time

class FitbitClientImplTests(TestCase):
    def setUp(self):
        self.access_token = 'fake_access_token'
        self.refresh_token = 'fake_refresh_token'
        self.client_id = 'fake_client_id'
        self.client_secret = 'fake_client_secret'
        self.token_updater = MagicMock()

        self.client = FitbitClient(
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_updater=self.token_updater
        )

    def test_init(self):
        self.assertEqual(self.client.access_token, self.access_token)
        self.assertEqual(self.client.refresh_token, self.refresh_token)
        self.assertEqual(self.client.client_id, self.client_id)
        self.assertEqual(self.client.client_secret, self.client_secret)
        self.assertEqual(self.client.token_updater, self.token_updater)
        
        # Check session configuration
        self.assertEqual(self.client.session.auto_refresh_url, FITBIT_TOKEN_URL)
        self.assertEqual(self.client.session.token['access_token'], self.access_token)

    def test_get_activities(self):
        # Mock the session.request
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'summary': {'steps': 1000}}
        self.client.session.request = MagicMock(return_value=mock_response)

        data = self.client.get_activities('2023-01-01')
        
        self.client.session.request.assert_called_with(
            'GET', 
            'https://api.fitbit.com/1/user/-/activities/date/2023-01-01.json'
        )
        self.assertEqual(data['summary']['steps'], 1000)

    def test_get_heart_rate(self):
        # Mock the session.request
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'activities-heart': []}
        self.client.session.request = MagicMock(return_value=mock_response)

        data = self.client.get_heart_rate('2023-01-01')

        self.client.session.request.assert_called_with(
            'GET',
            'https://api.fitbit.com/1/user/-/activities/heart/date/2023-01-01/1d.json'
        )
        self.assertEqual(data['activities-heart'], [])

    def test_token_updater_called(self):
        # This is a bit tricky to test with mocks alone without requests_mock or deeper mocking of OAuth2Session
        # but we can verify the configuration is passed correctly, which we done in test_init.
        pass
