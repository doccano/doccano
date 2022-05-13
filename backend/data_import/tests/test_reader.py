import unittest
from unittest.mock import MagicMock

import pandas as pd
from pandas.testing import assert_frame_equal

from data_import.pipeline.readers import FILE_NAME_COLUMN, LINE_NUM_COLUMN, Reader


class TestReader(unittest.TestCase):
    def setUp(self):
        self.parser = MagicMock()
        self.parser.parse.return_value = [{"a": 1}, {"a": 2}]
        filename = MagicMock()
        self.filenames = MagicMock()
        self.filenames.__iter__.return_value = [filename]
        self.rows = [
            {LINE_NUM_COLUMN: 1, FILE_NAME_COLUMN: filename, "a": 1},
            {LINE_NUM_COLUMN: 2, FILE_NAME_COLUMN: filename, "a": 2},
        ]

    def test_iter_method(self):
        reader = Reader(self.filenames, self.parser)
        self.assertEqual(list(reader), self.rows)

    def test_batch(self):
        reader = Reader(self.filenames, self.parser)
        batch = next(reader.batch(2))
        expected_df = pd.DataFrame(self.rows)
        assert_frame_equal(batch, expected_df)
