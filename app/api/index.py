from django_elasticsearch_dsl.documents import Document as ElasticsearchDocument
from django_elasticsearch_dsl.registries import registry
from django.conf import settings
from .models import Document


@registry.register_document
class DocumentIndex(ElasticsearchDocument):
    class Index:
        name = settings.ELASTIC_SEARCH_INDEX
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': settings.ELASTIC_SEARCH_SHARDS,
                    'number_of_replicas': settings.ELASTIC_SEARCH_REPLICAS}

    class Django:
        model = Document
        fields = [
            'text'
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000
