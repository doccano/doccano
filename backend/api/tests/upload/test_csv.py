import os
import shutil
import tempfile
import unittest

from ...views.upload.data import TextData
from ...views.upload.dataset import CsvDataset
from ...views.upload.label import CategoryLabel


class TestCsvDataset(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test_file.csv')

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
        content = 'label,text\nLabel,Text'
        dataset = CsvDataset(filenames=[], label_class=CategoryLabel, data_class=TextData)
        self.assert_record(content, dataset)

    def test_can_change_delimiter(self):
        content = 'label\ttext\nLabel\tText'
        dataset = CsvDataset(filenames=[], label_class=CategoryLabel, data_class=TextData, delimiter='\t')
        self.assert_record(content, dataset)

    def test_can_specify_column_name(self):
        content = 'star,body\nLabel,Text'
        dataset = CsvDataset(filenames=[], label_class=CategoryLabel, data_class=TextData,
                             column_data='body', column_label='star')
        self.assert_record(content, dataset)

    def test_can_load_only_text_column(self):
        content = 'star,text\nLabel,Text'
        dataset = CsvDataset(filenames=[], label_class=CategoryLabel, data_class=TextData)
        self.assert_record(content, dataset, label=[])

    def test_does_not_match_column_and_row(self):
        content = 'text,label\nText'
        dataset = CsvDataset(filenames=[], label_class=CategoryLabel, data_class=TextData)
        self.assert_record(content, dataset, label=[])
