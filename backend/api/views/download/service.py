from .repositories import BaseRepository
from .writer import BaseWriter


class ExportApplicationService:

    def __init__(self, repository: BaseRepository, writer: BaseWriter):
        self.repository = repository
        self.writer = writer

    def export(self, export_approved=False) -> str:
        records = self.repository.list(export_approved=export_approved)
        filepath = self.writer.write(records)
        return filepath
