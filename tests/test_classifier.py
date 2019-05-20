import os
import unittest

from doccano.app.classifier import run


class TestClassifier(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.filename = os.path.join(os.path.dirname(__file__), 'data/testdata.jsonl')

    def test_task_runner(self):
        run(self.filename)
