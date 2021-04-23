import os

from django.contrib.auth.models import User
from django.test import override_settings
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ...exceptions import FileParseException
from ...utils import (CoNLLParser, CSVParser, FastTextParser, JSONParser,
                      PlainTextParser)
from .utils import DATA_DIR, create_default_roles


class TestFeatures(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_name = 'user_name'
        cls.user_pass = 'user_pass'
        create_default_roles()
        cls.user = User.objects.create_user(username=cls.user_name, password=cls.user_pass, email='fizz@buzz.com')

    def setUp(self):
        self.client.login(username=self.user_name, password=self.user_pass)

    @override_settings(CLOUD_BROWSER_APACHE_LIBCLOUD_PROVIDER=None)
    def test_no_cloud_upload(self):
        response = self.client.get(reverse('features'))

        self.assertFalse(response.json().get('cloud_upload'))


@override_settings(IMPORT_BATCH_SIZE=2)
class TestParser(APITestCase):

    def parser_helper(self, filename, parser, include_label=True):
        with open(os.path.join(DATA_DIR, filename), mode='rb') as f:
            result = list(parser.parse(f))
            for data in result:
                for r in data:
                    self.assertIn('text', r)
                    if include_label:
                        self.assertIn('labels', r)
        return result

    def test_give_valid_data_to_conll_parser(self):
        self.parser_helper(filename='labeling.conll', parser=CoNLLParser())

    def test_give_valid_data_to_conll_parser_with_trailing_newlines(self):
        result = self.parser_helper(filename='labeling.trailing.conll', parser=CoNLLParser())
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 1)

    def test_plain_parser(self):
        self.parser_helper(filename='example.txt', parser=PlainTextParser(), include_label=False)

    def test_give_invalid_data_to_conll_parser(self):
        with self.assertRaises(FileParseException):
            self.parser_helper(filename='labeling.invalid.conll',
                               parser=CoNLLParser())

    def test_give_classification_data_to_csv_parser(self):
        self.parser_helper(filename='example.csv', parser=CSVParser(), include_label=False)

    def test_give_seq2seq_data_to_csv_parser(self):
        self.parser_helper(filename='example.csv', parser=CSVParser(), include_label=False)

    def test_give_classification_data_to_json_parser(self):
        self.parser_helper(filename='classification.jsonl', parser=JSONParser())

    def test_give_labeling_data_to_json_parser(self):
        self.parser_helper(filename='labeling.jsonl', parser=JSONParser())

    def test_give_seq2seq_data_to_json_parser(self):
        self.parser_helper(filename='seq2seq.jsonl', parser=JSONParser())

    def test_give_data_without_label_to_json_parser(self):
        self.parser_helper(filename='example.jsonl', parser=JSONParser(), include_label=False)

    def test_give_labeling_data_to_fasttext_parser(self):
        self.parser_helper(filename='example_fasttext.txt', parser=FastTextParser())

    def test_give_data_without_label_name_to_fasttext_parser(self):
        with self.assertRaises(FileParseException):
            self.parser_helper(filename='example_fasttext_label_tag_without_name.txt', parser=FastTextParser())

    def test_give_data_without_text_to_fasttext_parser(self):
        with self.assertRaises(FileParseException):
            self.parser_helper(filename='example_fasttext_without_text.txt', parser=FastTextParser())
