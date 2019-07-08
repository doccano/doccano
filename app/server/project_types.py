from django.contrib.staticfiles.storage import staticfiles_storage
from classifier.text.text_classifier import run_model_on_file as text_classifier_function
# from classifier.image.imagenet_classifier import run_model_on_file as imagenet_classifier_function

project_types = {
    'DocumentClassification': {
        'title': 'document classification',
        'type': 'DocumentClassification',
        'image': staticfiles_storage.url('images/cat-1045782_640.jpg'),
        'template_html': 'annotation/document_classification.html',
        'document_serializer': '',
        'annotations_serializer': '',
        'active_learning_function': text_classifier_function
    },

    'SequenceLabeling': {
        'title': 'sequence labeling',
        'type': 'SequenceLabeling',
        'image': staticfiles_storage.url('images/cat-3449999_640.jpg'),
        'template_html': 'annotation/sequence_labeling.html',
        'document_serializer': '',
        'annotations_serializer': '',
    },

    'Seq2seq': {
        'title': 'sequence to sequence',
        'type': 'Seq2seq',
        'image': staticfiles_storage.url('images/tiger-768574_640.jpg'),
        'template_html': 'annotation/seq2seq.html',
        'document_serializer': '',
        'annotations_serializer': '',
    },

    'ImageClassification': {
        'title': 'image classification',
        'type': 'DocumentClassification',
        'image': staticfiles_storage.url('images/cat-1045782_640.jpg'),
        'template_html': 'annotation/image_classification.html',
        'document_serializer': '',
        'annotations_serializer': '',
        # 'active_learning_function': imagenet_classifier_function
    },

    'ImageCaptioning': {
        'title': 'image captioning',
        'type': 'Seq2seq',
        'image': staticfiles_storage.url('images/cat-1045782_640.jpg'),
        'template_html': 'annotation/image_captioning.html',
        'document_serializer': '',
        'annotations_serializer': '',
    },
}
DOCUMENT_CLASSIFICATION = 'DocumentClassification'
SEQUENCE_LABELING = 'SequenceLabeling'
Seq2seq = 'Seq2seq'
