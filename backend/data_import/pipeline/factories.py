from .catalog import (
    CSV,
    JSON,
    JSONL,
    AudioFile,
    CoNLL,
    Excel,
    FastText,
    ImageFile,
    TextFile,
    TextLine,
)
from .parsers import (
    CoNLLParser,
    CSVParser,
    ExcelParser,
    FastTextParser,
    JSONLParser,
    JSONParser,
    LineParser,
    PlainParser,
    TextFileParser,
)


def create_parser(file_format: str, **kwargs):
    mapping = {
        TextFile.name: TextFileParser,
        TextLine.name: LineParser,
        CSV.name: CSVParser,
        JSONL.name: JSONLParser,
        JSON.name: JSONParser,
        FastText.name: FastTextParser,
        Excel.name: ExcelParser,
        CoNLL.name: CoNLLParser,
        ImageFile.name: PlainParser,
        AudioFile.name: PlainParser,
    }
    if file_format not in mapping:
        raise ValueError(f"Invalid format: {file_format}")
    return mapping[file_format](**kwargs)
