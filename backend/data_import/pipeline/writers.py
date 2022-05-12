from .readers import BaseReader
from projects.models import Project


class Writer:
    def __init__(self, batch_size: int):
        self.batch_size = batch_size

    def save(self, reader: BaseReader, project: Project, user, labeled_examples):
        for batch in reader.batch(self.batch_size, labeled_examples):
            batch.create(project, user)
