from django.test import TestCase


class SmokeTest(TestCase):
    #sprawdzamy czy test odpali się sam?
    def test_bad_maths(self):
        self.assertEqual(2+2, 5)
