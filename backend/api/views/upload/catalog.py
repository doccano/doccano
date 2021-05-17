from collections import defaultdict
from typing import Dict, List, Type

from pydantic import BaseModel
from typing_extensions import Literal

from ...models import (DOCUMENT_CLASSIFICATION, IMAGE_CLASSIFICATION, SEQ2SEQ,
                       SEQUENCE_LABELING)
from . import examples

encodings = Literal[
    'Auto',
    'ascii',
    'big5',
    'big5hkscs',
    'cp037',
    'cp273',
    'cp424',
    'cp437',
    'cp500',
    'cp720',
    'cp737',
    'cp775',
    'cp850',
    'cp852',
    'cp855',
    'cp856',
    'cp857',
    'cp858',
    'cp860',
    'cp861',
    'cp862',
    'cp863',
    'cp864',
    'cp865',
    'cp866',
    'cp869',
    'cp874',
    'cp875',
    'cp932',
    'cp949',
    'cp950',
    'cp1006',
    'cp1026',
    'cp1125',
    'cp1140',
    'cp1250',
    'cp1251',
    'cp1252',
    'cp1253',
    'cp1254',
    'cp1255',
    'cp1256',
    'cp1257',
    'cp1258',
    'cp65001',
    'euc_jp',
    'euc_jis_2004',
    'euc_jisx0213',
    'euc_kr',
    'gb2312',
    'gbk',
    'gb18030',
    'hz',
    'iso2022_jp',
    'iso2022_jp_1',
    'iso2022_jp_2',
    'iso2022_jp_2004',
    'iso2022_jp_3',
    'iso2022_jp_ext',
    'iso2022_kr',
    'latin_1',
    'iso8859_2',
    'iso8859_3',
    'iso8859_4',
    'iso8859_5',
    'iso8859_6',
    'iso8859_7',
    'iso8859_8',
    'iso8859_9',
    'iso8859_10',
    'iso8859_11',
    'iso8859_13',
    'iso8859_14',
    'iso8859_15',
    'iso8859_16',
    'johab',
    'koi8_r',
    'koi8_t',
    'koi8_u',
    'kz1048',
    'mac_cyrillic',
    'mac_greek',
    'mac_iceland',
    'mac_latin2',
    'mac_roman',
    'mac_turkish',
    'ptcp154',
    'shift_jis',
    'shift_jis_2004',
    'shift_jisx0213',
    'utf_32',
    'utf_32_be',
    'utf_32_le',
    'utf_16',
    'utf_16_be',
    'utf_16_le',
    'utf_7',
    'utf_8',
    'utf_8_sig'
]


class Format:
    name = ''
    accept_types = ''

    @classmethod
    def dict(cls):
        return {
            'name': cls.name,
            'accept_types': cls.accept_types
        }


class CSV(Format):
    name = 'CSV'
    accept_types = 'text/csv'


class FastText(Format):
    name = 'fastText'
    accept_types = 'text/plain'


class JSON(Format):
    name = 'JSON'
    accept_types = 'application/json'


class JSONL(Format):
    name = 'JSONL'
    accept_types = '*'


class Excel(Format):
    name = 'Excel'
    accept_types = 'application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


class TextFile(Format):
    name = 'TextFile'
    accept_types = 'text/*'


class TextLine(Format):
    name = 'TextLine'
    accept_types = 'text/*'


class CoNLL(Format):
    name = 'CoNLL'
    accept_types = 'text/*'


class ImageFile(Format):
    name = 'ImageFile'
    accept_types = 'image/png, image/jpeg, image/bmp, image/gif'


class OptionColumn(BaseModel):
    encoding: encodings = 'utf_8'
    column_data: str = 'text'
    column_label: str = 'label'


class OptionDelimiter(OptionColumn):
    encoding: encodings = 'utf_8'
    delimiter: Literal[',', '\t', ';', '|', ' '] = ','


class OptionEncoding(BaseModel):
    encoding: encodings = 'utf_8'


class OptionCoNLL(BaseModel):
    encoding: encodings = 'utf_8'
    scheme: Literal['IOB2', 'IOE2', 'IOBES', 'BILOU'] = 'IOB2'
    delimiter: Literal[' ', ''] = ' '


class OptionNone(BaseModel):
    pass


class Options:
    options: Dict[str, List] = defaultdict(list)

    @classmethod
    def filter_by_task(cls, task_name: str):
        options = cls.options[task_name]
        return [
            {
                **format.dict(),
                **option.schema(),
                'example': example
            } for format, option, example in options
        ]

    @classmethod
    def register(cls,
                 task: str,
                 format: Type[Format],
                 option: Type[BaseModel],
                 example: str):
        cls.options[task].append((format, option, example))


# Text Classification
Options.register(DOCUMENT_CLASSIFICATION, TextFile, OptionEncoding, examples.Generic_TextFile)
Options.register(DOCUMENT_CLASSIFICATION, TextLine, OptionEncoding, examples.Generic_TextLine)
Options.register(DOCUMENT_CLASSIFICATION, CSV, OptionDelimiter, examples.Category_CSV)
Options.register(DOCUMENT_CLASSIFICATION, FastText, OptionEncoding, examples.Category_fastText)
Options.register(DOCUMENT_CLASSIFICATION, JSON, OptionColumn, examples.Category_JSON)
Options.register(DOCUMENT_CLASSIFICATION, JSONL, OptionColumn, examples.Category_JSONL)
Options.register(DOCUMENT_CLASSIFICATION, Excel, OptionColumn, examples.Category_CSV)

# Sequence Labeling
Options.register(SEQUENCE_LABELING, TextFile, OptionEncoding, examples.Generic_TextFile)
Options.register(SEQUENCE_LABELING, TextLine, OptionEncoding, examples.Generic_TextLine)
Options.register(SEQUENCE_LABELING, JSONL, OptionColumn, examples.Offset_JSONL)
Options.register(SEQUENCE_LABELING, CoNLL, OptionCoNLL, examples.Offset_CoNLL)

# Sequence to sequence
Options.register(SEQ2SEQ, TextFile, OptionEncoding, examples.Generic_TextFile)
Options.register(SEQ2SEQ, TextLine, OptionEncoding, examples.Generic_TextLine)
Options.register(SEQ2SEQ, CSV, OptionDelimiter, examples.Text_CSV)
Options.register(SEQ2SEQ, JSON, OptionColumn, examples.Text_JSON)
Options.register(SEQ2SEQ, JSONL, OptionColumn, examples.Text_JSONL)
Options.register(SEQ2SEQ, Excel, OptionColumn, examples.Text_CSV)

# Image classification
Options.register(IMAGE_CLASSIFICATION, ImageFile, OptionNone, examples.Generic_ImageFile)
