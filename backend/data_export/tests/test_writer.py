import json
import unittest
from unittest.mock import call, patch

from ..pipeline.data import Record
from ..pipeline.writers import CsvWriter, IntentAndSlotWriter


class TestCSVWriter(unittest.TestCase):
    def setUp(self):
        self.records = [
            Record(data_id=0, data="exampleA", label=["labelA"], user="admin", metadata={"hidden": "secretA"}),
            Record(data_id=1, data="exampleB", label=["labelB"], user="admin", metadata={"hidden": "secretB"}),
            Record(data_id=2, data="exampleC", label=["labelC"], user="admin", metadata={"meta": "secretC"}),
        ]

    def test_create_header(self):
        writer = CsvWriter(".")
        header = writer.create_header(self.records)
        expected = ["id", "data", "label", "hidden", "meta"]
        self.assertEqual(header, expected)

    def test_create_line(self):
        writer = CsvWriter(".")
        record = self.records[0]
        line = writer.create_line(record)
        expected = {"id": record.id, "data": record.data, "label": record.label[0], "hidden": "secretA"}
        self.assertEqual(line, expected)

    def test_label_order(self):
        writer = CsvWriter(".")
        record1 = Record(data_id=0, data="", label=["labelA", "labelB"], user="", metadata={})
        record2 = Record(data_id=0, data="", label=["labelB", "labelA"], user="", metadata={})
        line1 = writer.create_line(record1)
        line2 = writer.create_line(record2)
        expected = "labelA#labelB"
        self.assertEqual(line1["label"], expected)
        self.assertEqual(line2["label"], expected)

    @patch("os.remove")
    @patch("zipfile.ZipFile")
    @patch("csv.DictWriter.writerow")
    @patch("builtins.open")
    def test_dump(self, mock_open_file, csv_io, zip_io, mock_remove_file):
        writer = CsvWriter(".")
        writer.write(self.records)

        self.assertEqual(mock_open_file.call_count, 1)
        mock_open_file.assert_called_with("./admin.csv", mode="a", encoding="utf-8")

        self.assertEqual(csv_io.call_count, len(self.records) + 1)  # +1 is for a header
        calls = [
            call({"id": "id", "data": "data", "label": "label", "hidden": "hidden", "meta": "meta"}),
            call({"id": 0, "data": "exampleA", "label": "labelA", "hidden": "secretA"}),
            call({"id": 1, "data": "exampleB", "label": "labelB", "hidden": "secretB"}),
            call({"id": 2, "data": "exampleC", "label": "labelC", "meta": "secretC"}),
        ]
        csv_io.assert_has_calls(calls)


class TestIntentWriter(unittest.TestCase):
    def setUp(self):
        self.record = Record(
            data_id=0,
            data="exampleA",
            label={"cats": ["positive"], "entities": [(0, 1, "LOC")]},
            user="admin",
            metadata={},
        )

    def test_create_line(self):
        writer = IntentAndSlotWriter(".")
        actual = writer.create_line(self.record)
        expected = {
            "id": self.record.id,
            "text": self.record.data,
            "cats": ["positive"],
            "entities": [[0, 1, "LOC"]],
        }
        self.assertEqual(json.loads(actual), expected)
