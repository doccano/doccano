from typing import Any, Dict


class FileImportException(Exception):
    def dict(self) -> Dict[str, Any]:
        raise NotImplementedError()


class FileParseException(FileImportException):
    def __init__(self, filename: str, line_num: int, message: str):
        self.filename = filename
        self.line_num = line_num
        self.message = message

    def __str__(self):
        return f"ParseError: You cannot parse line {self.line_num} in {self.filename}: {self.message}"

    def dict(self):
        return {"filename": self.filename, "line": self.line_num, "message": self.message}


class MaximumFileSizeException(FileImportException):
    def __init__(self, filename: str, max_size: int):
        self.filename = filename
        self.max_size = max_size

    def __str__(self):
        return f"The maximum file size that can be uploaded is {self.max_size/1024/1024} MB"

    def dict(self):
        return {"filename": self.filename, "line": -1, "message": str(self)}


class FileTypeException(FileImportException):
    def __init__(self, filename: str, filetype: str, allowed_types=None):
        self.filename = filename
        self.filetype = filetype
        self.allowed_types = allowed_types

    def __str__(self):
        return f"The file type {self.filetype} is unexpected. Expected: {self.allowed_types}"

    def dict(self):
        return {"filename": self.filename, "line": -1, "message": str(self)}


class FileFormatException(FileImportException):
    def __init__(self, file_format: str):
        self.file_format = file_format

    def dict(self):
        message = f"Unknown file format: {self.file_format}"
        return {"message": message}
