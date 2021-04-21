class FileParseException(Exception):

    def __init__(self, filename: str, line_num: int, message: str):
        self.filename = filename
        self.line_num = line_num
        self.message = message

    def __str__(self):
        return f'ParseError: You cannot parse line {self.line_num} in {self.filename}: {self.message}'

    def dict(self):
        return {
            'filename': self.filename,
            'line': self.line_num,
            'message': self.message
        }
