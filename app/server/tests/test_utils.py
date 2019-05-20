from django.test import TestCase

from server.utils import Color


class TestColor(TestCase):
    def test_random_color(self):
        color = Color.random()
        self.assertTrue(0 <= color.red <= 255)
        self.assertTrue(0 <= color.green <= 255)
        self.assertTrue(0 <= color.blue <= 255)

    def test_hex(self):
        color = Color(red=255, green=192, blue=203)
        self.assertEqual(color.hex, '#ffc0cb')

    def test_contrast_color(self):
        color = Color(red=255, green=192, blue=203)
        self.assertEqual(color.contrast_color.hex, '#000000')

        color = Color(red=199, green=21, blue=133)
        self.assertEqual(color.contrast_color.hex, '#ffffff')
