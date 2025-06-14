import unittest

from ..pipeline.catalog import Options
from projects.models import ProjectType


class TestOptions(unittest.TestCase):
    def test_return_at_least_one_option(self):
        for task in ProjectType:
            with self.subTest(task=task):
                options = Options.filter_by_task(task)
                self.assertGreaterEqual(len(options), 1)
