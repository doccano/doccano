from .readers import BaseReader
from examples.models import Example
from projects.models import Project


class Writer:
    def __init__(self, batch_size: int):
        self.batch_size = batch_size

    def save(self, reader: BaseReader, project: Project, user):
        for batch in reader.batch(self.batch_size):
            # write examples to database
            examples = batch.create_data(project)
            examples = Example.objects.bulk_create(examples)

            # write label types to database
            label_types = batch.create_label_type(project)
            for label_type_class, instances in label_types.items():
                label_type_class.objects.bulk_create(instances, ignore_conflicts=True)

            # write labels to database
            labels = batch.create_label(project, user, examples)
            for label_class, instances in labels.items():
                label_class.objects.bulk_create(instances)
