from apps.account.tests.test_setup import TestSetUp

from apps.account.models import *

class TestViews(TestSetUp):
    def test_roles(self):
        self.assertEqual(Role.objects.all().count(),4)