import os
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from ..pipeline.writers import CsvWriter, JsonlWriter, JsonWriter


class TestWriter(unittest.TestCase):
    def setUp(self):
        self.dataset = pd.DataFrame(
            [
                {"id": 0, "text": "A"},
                {"id": 1, "text": "B"},
                {"id": 2, "text": "C"},
            ]
        )
        self.file = "tmp.csv"

    def tearDown(self):
        os.remove(self.file)


class TestCSVWriter(TestWriter):
    def test_write(self):
        writer = CsvWriter()
        writer.write(self.file, self.dataset)
        loaded_dataset = pd.read_csv(self.file)
        assert_frame_equal(self.dataset, loaded_dataset)


class TestJsonWriter(TestWriter):
    def test_write(self):
        writer = JsonWriter()
        writer.write(self.file, self.dataset)
        loaded_dataset = pd.read_json(self.file)
        assert_frame_equal(self.dataset, loaded_dataset)


class TestJsonlWriter(TestWriter):
    def test_write(self):
        writer = JsonlWriter()
        writer.write(self.file, self.dataset)
        loaded_dataset = pd.read_json(self.file, lines=True)
        assert_frame_equal(self.dataset, loaded_dataset)
