from django.test import TestCase , SimpleTestCase
from User.models import User

class TestExample(TestCase):
    def test_view_home(self):
        # response = self.client.get('')
        user = User.objects.create_user('ali','www','123')
        self.assertNotEqual(None,user)
