import json
import os
import shutil
import tempfile
import unittest

from data_import.pipeline import parsers
from data_import.pipeline.readers import LINE_NUMBER_COLUMN


class TestParser(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_file.csv")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_file(self, content):
        with open(self.test_file, "w") as f:
            f.write(content)

    def assert_record(self, content, parser, expected):
        self.create_file(content)
        it = parser.parse(self.test_file)
        for expect in expected:
            row = next(it)
            row.pop(LINE_NUMBER_COLUMN, None)
            self.assertEqual(row, expect)
        with self.assertRaises(StopIteration):
            next(it)


class TestPlainParser(TestParser):
    def test_read(self):
        content = "example"
        parser = parsers.PlainParser()
        expected = [{}]
        self.assert_record(content, parser, expected)


class TestLineParser(TestParser):
    def test_read(self):
        content = "Hello, World!\nこんにちは"
        parser = parsers.LineParser()
        expected = [{"text": "Hello, World!"}, {"text": "こんにちは"}]
        self.assert_record(content, parser, expected)


class TestTextFileParser(TestParser):
    def test_read(self):
        content = "Hello, World!\nこんにちは"
        parser = parsers.TextFileParser()
        expected = [{"text": content}]
        self.assert_record(content, parser, expected)


class TestCsvParser(TestParser):
    def test_read(self):
        content = "label,text\nLabel,Text"
        parser = parsers.CSVParser(delimiter=",")
        expected = [{"label": "Label", "text": "Text"}]
        self.assert_record(content, parser, expected)

    def test_can_change_delimiter(self):
        content = "label\ttext\nLabel\tText"
        parser = parsers.CSVParser(delimiter="\t")
        expected = [{"label": "Label", "text": "Text"}]
        self.assert_record(content, parser, expected)

    def test_can_read_null_value(self):
        content = "text,label\nText"
        parser = parsers.CSVParser(delimiter=",")
        expected = [{"text": "Text", "label": None}]
        self.assert_record(content, parser, expected)


class TestJSONParser(TestParser):
    def test_read(self):
        content = json.dumps([{"text": "line1", "labels": "Label1"}, {"text": "line2", "labels": "Label2"}])
        parser = parsers.JSONParser()
        expected = json.loads(content)
        self.assert_record(content, parser, expected)


class TestJSONLParser(TestParser):
    def test_read(self):
        line1 = json.dumps({"text": "line1", "labels": "Label1"})
        line2 = json.dumps({"text": "line2", "labels": "Label2"})
        content = f"{line1}\n{line2}"
        parser = parsers.JSONLParser()
        expected = [json.loads(line1), json.loads(line2)]
        self.assert_record(content, parser, expected)


class TestFastTextParser(TestParser):
    def test_read(self):
        content = "__label__sauce __label__cheese Text"
        parser = parsers.FastTextParser()
        expected = [{"text": "Text", "label": ["sauce", "cheese"]}]
        self.assert_record(content, parser, expected)


class TestCoNLLParser(TestParser):
    def test_can_read(self):
        content = """EU\tB-ORG
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
        parser = parsers.CoNLLParser()
        expected = [
            {
                "text": "EU rejects German call to boycott British lamb .",
                "label": [(0, 2, "ORG"), (11, 17, "MISC"), (34, 41, "MISC")],
            },
            {"text": "Peter Blackburn", "label": [(0, 15, "PER")]},
        ]
        self.assert_record(content, parser, expected)
