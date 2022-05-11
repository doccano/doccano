from .readers import BaseReader
from projects.models import Project


class Writer:
    def __init__(self, batch_size: int):
        self.batch_size = batch_size

    def save(self, reader: BaseReader, project: Project, user):
        for batch in reader.batch(self.batch_size):
            examples = batch.create_data(project)
            batch.create_label_type(project)
            batch.create_label(project, user, examples)
