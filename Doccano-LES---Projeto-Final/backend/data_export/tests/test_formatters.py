import unittest
from unittest.mock import MagicMock

import pandas as pd
from pandas.testing import assert_frame_equal

from data_export.models import DATA
from data_export.pipeline.formatters import (
    DictFormatter,
    FastTextCategoryFormatter,
    JoinedCategoryFormatter,
    ListedCategoryFormatter,
    RenameFormatter,
    TupledSpanFormatter,
)

TARGET_COLUMN = "labels"


class TestDictFormatter(unittest.TestCase):
    def setUp(self):
        self.return_value = {"label": "Label"}
        label = MagicMock()
        label.to_dict.return_value = self.return_value
        self.dataset = pd.DataFrame([{TARGET_COLUMN: [label]}])

    def test_format(self):
        formatter = DictFormatter(TARGET_COLUMN)
        dataset = formatter.format(self.dataset)
        expected_dataset = pd.DataFrame([{TARGET_COLUMN: [self.return_value]}])
        assert_frame_equal(dataset, expected_dataset)


class TestJoinedCategoryFormatter(unittest.TestCase):
    def setUp(self):
        self.return_value = "Label"
        label = MagicMock()
        label.to_string.return_value = self.return_value
        self.dataset = pd.DataFrame([{TARGET_COLUMN: [label]}])

    def test_format(self):
        formatter = JoinedCategoryFormatter(TARGET_COLUMN)
        dataset = formatter.format(self.dataset)
        expected_dataset = pd.DataFrame([{TARGET_COLUMN: self.return_value}])
        assert_frame_equal(dataset, expected_dataset)


class TestListedCategoryFormatter(unittest.TestCase):
    def setUp(self):
        self.return_value = "Label"
        label = MagicMock()
        label.to_string.return_value = self.return_value
        self.dataset = pd.DataFrame([{TARGET_COLUMN: [label]}])

    def test_format(self):
        formatter = ListedCategoryFormatter(TARGET_COLUMN)
        dataset = formatter.format(self.dataset)
        expected_dataset = pd.DataFrame([{TARGET_COLUMN: [self.return_value]}])
        assert_frame_equal(dataset, expected_dataset)


class TestTupledSpanFormatter(unittest.TestCase):
    def setUp(self):
        self.return_value = (0, 1, "Label")
        label = MagicMock()
        label.to_tuple.return_value = self.return_value
        self.dataset = pd.DataFrame([{TARGET_COLUMN: [label]}])

    def test_format(self):
        formatter = TupledSpanFormatter(TARGET_COLUMN)
        dataset = formatter.format(self.dataset)
        expected_dataset = pd.DataFrame([{TARGET_COLUMN: [self.return_value]}])
        assert_frame_equal(dataset, expected_dataset)


class TestFastTextFormatter(unittest.TestCase):
    def setUp(self):
        self.return_value_label = "Label"
        self.return_value_comment = "Comment"
        label = MagicMock()
        comment = MagicMock()
        label.to_string.return_value = self.return_value_label
        comment.to_string.return_value = self.return_value_comment
        self.dataset = pd.DataFrame([{TARGET_COLUMN: [label], DATA: "example", "Comments": [comment]}])

    def test_format(self):
        formatter = FastTextCategoryFormatter(TARGET_COLUMN)
        dataset = formatter.format(self.dataset)
        expected_dataset = pd.DataFrame(
            [f"__label__{self.return_value_label} example __comment__{self.return_value_comment}"]
        )
        self.assertEqual(dataset.to_csv(index=False, header=None), expected_dataset.to_csv(index=False, header=None))


class TestRenameFormatter(unittest.TestCase):
    def test_format(self):
        dataset = pd.DataFrame([{"data": "example"}])
        formatter = RenameFormatter(**{"data": "text"})
        dataset = formatter.format(dataset)
        expected_dataset = pd.DataFrame([{"text": "example"}])
        assert_frame_equal(dataset, expected_dataset)
