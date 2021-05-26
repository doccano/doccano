import os
import shutil
import tempfile
import unittest

from ...views.upload.data import TextData
from ...views.upload.dataset import FastTextDataset
from ...views.upload.label import CategoryLabel


class TestFastTextDataset(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test_file.txt')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_file(self, content):
        with open(self.test_file, 'w') as f:
            f.write(content)

    def assert_record(self, content, dataset, data='Text', label=None):
        if label is None:
            label = [{'text': 'Label'}]
        self.create_file(content)
        record = next(dataset.load(self.test_file))
        self.assertEqual(record.data['text'], data)
        self.assertEqual(record.label, label)

    def test_can_load_default_column_names(self):
        content = '__label__sauce __label__cheese Text'
        dataset = FastTextDataset(filenames=[], label_class=CategoryLabel, data_class=TextData)
        label = [{'text': 'sauce'}, {'text': 'cheese'}]
        self.assert_record(content, dataset, label=label)
