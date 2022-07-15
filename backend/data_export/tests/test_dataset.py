import unittest
from unittest.mock import MagicMock

import pandas as pd
from pandas.testing import assert_frame_equal

from data_export.pipeline.dataset import Dataset


class TestDataset(unittest.TestCase):
    def setUp(self):
        example = MagicMock()
        example.to_dict.return_value = {"data": "example"}
        self.examples = MagicMock()
        self.examples.__iter__.return_value = [example]
        label = MagicMock()
        label.find_by.return_value = {"labels": ["label"]}
        self.labels = MagicMock()
        self.labels.__iter__.return_value = [label]
        comment = MagicMock()
        comment.find_by.return_value = {"comments": ["comment"]}
        self.comments = MagicMock()
        self.comments.__iter__.return_value = [comment]

    def test_to_dataframe(self):
        dataset = Dataset(self.examples, self.labels, self.comments)
        df = dataset.to_dataframe()
        expected = pd.DataFrame([{"data": "example", "labels": ["label"], "comments": ["comment"]}])
        assert_frame_equal(df, expected)
