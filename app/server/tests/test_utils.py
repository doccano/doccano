import io

from django.test import TestCase

from seqeval.metrics.sequence_labeling import get_entities

from ..models import Label, Document
from ..utils import BaseStorage, ClassificationStorage, SequenceLabelingStorage, Seq2seqStorage, CoNLLParser
from ..utils import Color, iterable_to_io


class TestColor(TestCase):
    def test_random_color(self):
        color = Color.random()
        self.assertTrue(0 <= color.red <= 255)
        self.assertTrue(0 <= color.green <= 255)
        self.assertTrue(0 <= color.blue <= 255)

    def test_hex(self):
        color = Color(red=255, green=192, blue=203)
        self.assertEqual(color.hex, '#ffc0cb')

    def test_contrast_color(self):
        color = Color(red=255, green=192, blue=203)
        self.assertEqual(color.contrast_color.hex, '#000000')

        color = Color(red=199, green=21, blue=133)
        self.assertEqual(color.contrast_color.hex, '#ffffff')


class TestBaseStorage(TestCase):
    def test_extract_label(self):
        data = [{'labels': ['positive']}, {'labels': ['negative']}]

        actual = BaseStorage.extract_label(data)

        self.assertEqual(actual, [['positive'], ['negative']])

    def test_exclude_created_labels(self):
        labels = ['positive', 'negative']
        created = {'positive': Label(text='positive')}

        actual = BaseStorage.exclude_created_labels(labels, created)

        self.assertEqual(actual, ['negative'])

    def test_to_serializer_format(self):
        labels = ['positive']
        created = {}

        actual = BaseStorage.to_serializer_format(labels, created, random_seed=123)

        self.assertEqual(actual, [{
            'text': 'positive',
            'prefix_key': None,
            'suffix_key': 'p',
            'background_color': '#0d1668',
            'text_color': '#ffffff',
        }])

    def test_get_shortkey_without_existing_shortkey(self):
        label = 'positive'
        created = {}

        actual = BaseStorage.get_shortkey(label, created)

        self.assertEqual(actual, ('p', None))

    def test_get_shortkey_with_existing_shortkey(self):
        label = 'positive'
        created = {('p', None)}

        actual = BaseStorage.get_shortkey(label, created)

        self.assertEqual(actual, ('p', 'ctrl'))

    def test_update_saved_labels(self):
        saved = {'positive': Label(text='positive', text_color='#000000')}
        new = [Label(text='positive', text_color='#ffffff')]

        actual = BaseStorage.update_saved_labels(saved, new)

        self.assertEqual(actual['positive'].text_color, '#ffffff')


class TestClassificationStorage(TestCase):
    def test_extract_unique_labels(self):
        labels = [['positive'], ['positive', 'negative'], ['negative']]

        actual = ClassificationStorage.extract_unique_labels(labels)

        self.assertCountEqual(actual, ['positive', 'negative'])

    def test_make_annotations(self):
        docs = [Document(text='a', id=1), Document(text='b', id=2), Document(text='c', id=3)]
        labels = [['positive'], ['positive', 'negative'], ['negative']]
        saved_labels = {'positive': Label(text='positive', id=1), 'negative': Label(text='negative', id=2)}

        actual = ClassificationStorage.make_annotations(docs, labels, saved_labels)

        self.assertCountEqual(actual, [
            {'document': 1, 'label': 1},
            {'document': 2, 'label': 1},
            {'document': 2, 'label': 2},
            {'document': 3, 'label': 2},
        ])


class TestSequenceLabelingStorage(TestCase):
    def test_extract_unique_labels(self):
        labels = [[[0, 1, 'LOC']], [[3, 4, 'ORG']]]

        actual = SequenceLabelingStorage.extract_unique_labels(labels)

        self.assertCountEqual(actual, ['LOC', 'ORG'])

    def test_make_annotations(self):
        docs = [Document(text='a', id=1), Document(text='b', id=2)]
        labels = [[[0, 1, 'LOC']], [[3, 4, 'ORG']]]
        saved_labels = {'LOC': Label(text='LOC', id=1), 'ORG': Label(text='ORG', id=2)}

        actual = SequenceLabelingStorage.make_annotations(docs, labels, saved_labels)

        self.assertEqual(actual, [
            {'document': 1, 'label': 1, 'start_offset': 0, 'end_offset': 1},
            {'document': 2, 'label': 2, 'start_offset': 3, 'end_offset': 4},
        ])


class TestSeq2seqStorage(TestCase):
    def test_make_annotations(self):
        docs = [Document(text='a', id=1), Document(text='b', id=2)]
        labels = [['Hello!'], ['How are you?', "What's up?"]]

        actual = Seq2seqStorage.make_annotations(docs, labels)

        self.assertEqual(actual, [
            {'document': 1, 'text': 'Hello!'},
            {'document': 2, 'text': 'How are you?'},
            {'document': 2, 'text': "What's up?"},
        ])


class TestCoNLLParser(TestCase):
    def test_calc_char_offset(self):
        words = ['EU', 'rejects', 'German', 'call']
        tags = ['B-ORG', 'O', 'B-MISC', 'O']

        entities = get_entities(tags)
        actual = CoNLLParser.calc_char_offset(words, tags)

        self.assertEqual(entities, [('ORG', 0, 0), ('MISC', 2, 2)])

        self.assertEqual(actual, {
            'text': 'EU rejects German call',
            'labels': [[0, 2, 'ORG'], [11, 17, 'MISC']]
        })


class TestIterableToIO(TestCase):
    def test(self):
        def iterable():
            yield b'fo'
            yield b'o\nbar\n'
            yield b'baz\nrest'

        stream = iterable_to_io(iterable())
        stream = io.TextIOWrapper(stream)

        self.assertEqual(stream.readlines(), ['foo\n', 'bar\n', 'baz\n', 'rest'])
