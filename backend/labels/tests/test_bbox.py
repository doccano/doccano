from django.db import IntegrityError
from django.test import TestCase
from model_mommy import mommy

from projects.tests.utils import prepare_project


class TestBoundingBox(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project = prepare_project()
        cls.example = mommy.make("Example", project=cls.project.item)
        cls.user = cls.project.admin

    def test_cannot_create_label_if_x_is_less_than_zero(self):
        with self.assertRaises(IntegrityError):
            mommy.make("BoundingBox", example=self.example, x=-1, y=0, width=0, height=0)

    def test_cannot_create_label_if_y_is_less_than_zero(self):
        with self.assertRaises(IntegrityError):
            mommy.make("BoundingBox", example=self.example, x=0, y=-1, width=0, height=0)

    def test_cannot_create_label_if_width_is_less_than_zero(self):
        with self.assertRaises(IntegrityError):
            mommy.make("BoundingBox", example=self.example, x=0, y=0, width=-1, height=0)

    def test_cannot_create_label_if_height_is_less_than_zero(self):
        with self.assertRaises(IntegrityError):
            mommy.make("BoundingBox", example=self.example, x=0, y=0, width=0, height=-1)
