import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
from pandas.testing import assert_frame_equal

from data_import.pipeline.readers import (
    FILE_NAME_COLUMN,
    UPLOAD_NAME_COLUMN,
    UUID_COLUMN,
    Reader,
)


class TestReader(unittest.TestCase):
    def setUp(self):
        self.parser = MagicMock()
        self.parser.parse.return_value = [{"a": 1}, {"a": 2}]
        filename = MagicMock()
        filename.generated_name = "filename"
        filename.upload_name = "upload_name"
        self.filenames = MagicMock()
        self.filenames.__iter__.return_value = [filename]
        self.rows = [
            {
                UUID_COLUMN: "uuid",
                FILE_NAME_COLUMN: filename.generated_name,
                UPLOAD_NAME_COLUMN: filename.upload_name,
                "a": 1,
            },
            {
                UUID_COLUMN: "uuid",
                FILE_NAME_COLUMN: filename.generated_name,
                UPLOAD_NAME_COLUMN: filename.upload_name,
                "a": 2,
            },
        ]

    @patch("data_import.pipeline.readers.uuid.uuid4")
    def test_iter_method(self, mock):
        mock.return_value = "uuid"
        reader = Reader(self.filenames, self.parser)
        self.assertEqual(list(reader), self.rows)

    @patch("data_import.pipeline.readers.uuid.uuid4")
    def test_batch(self, mock):
        mock.return_value = "uuid"
        reader = Reader(self.filenames, self.parser)
        batch = next(reader.batch(2))
        expected_df = pd.DataFrame(self.rows)
        assert_frame_equal(batch, expected_df)
