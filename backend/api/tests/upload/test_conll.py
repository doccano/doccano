import os
import shutil
import tempfile
import unittest

from ...views.upload.data import TextData
from ...views.upload.dataset import CoNLLDataset
from ...views.upload.label import OffsetLabel


class TestCoNLLDataset(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test_file.txt')
        self.content = """EU\tB-ORG
rejects\tO
German\tB-MISC
call\tO
to\tO
boycott\tO
British\tB-MISC
lamb\tO
.\tO

Peter\tB-PER
Blackburn\tI-PER

"""

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_file(self, encoding=None):
        with open(self.test_file, 'w', encoding=encoding) as f:
            f.write(self.content)

    def test_can_load(self):
        self.create_file()
        dataset = CoNLLDataset(
            filenames=[self.test_file],
            label_class=OffsetLabel,
            data_class=TextData
        )
        it = dataset.load(self.test_file)
        record = next(it)
        expected = 'EU rejects German call to boycott British lamb .'
        self.assertEqual(record.data['text'], expected)
