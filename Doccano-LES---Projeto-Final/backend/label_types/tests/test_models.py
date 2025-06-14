from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from model_mommy import mommy

from label_types.models import CategoryType, generate_random_hex_color


class TestLabel(TestCase):
    def test_deny_creating_same_text(self):
        label = mommy.make("CategoryType")
        with self.assertRaises(IntegrityError):
            mommy.make("CategoryType", project=label.project, text=label.text)

    def test_keys_uniqueness(self):
        label = mommy.make("CategoryType", prefix_key="ctrl", suffix_key="a")
        with self.assertRaises(ValidationError):
            CategoryType(
                project=label.project, text="example", prefix_key=label.prefix_key, suffix_key=label.suffix_key
            ).full_clean()

    def test_suffix_key_uniqueness(self):
        label = mommy.make("CategoryType", prefix_key=None, suffix_key="a")
        with self.assertRaises(ValidationError):
            CategoryType(
                project=label.project, text="example", prefix_key=label.prefix_key, suffix_key=label.suffix_key
            ).full_clean()

    def test_cannot_add_label_only_prefix_key(self):
        project = mommy.make("Project")
        label = CategoryType(project=project, text="example", prefix_key="ctrl")
        with self.assertRaises(ValidationError):
            label.clean()

    def test_can_add_label_only_suffix_key(self):
        project = mommy.make("Project")
        label = CategoryType(project=project, text="example", suffix_key="a")
        try:
            label.full_clean()
        except ValidationError:
            self.fail(msg=ValidationError)

    def test_can_add_label_suffix_key_with_prefix_key(self):
        project = mommy.make("Project")
        label = CategoryType(project=project, text="example", prefix_key="ctrl", suffix_key="a")
        try:
            label.full_clean()
        except ValidationError:
            self.fail(msg=ValidationError)


class TestGeneratedColor(TestCase):
    def test_length(self):
        for _ in range(100):
            color = generate_random_hex_color()
            self.assertEqual(len(color), 7)
