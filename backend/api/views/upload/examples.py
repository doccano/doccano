Generic_TextFile = """
├── 202104210943.txt
├── 202104210944.txt
└── 202104210945.txt
"""

Generic_ImageFile = """
├── 202104210943.png
├── 202104210944.png
└── 202104210945.png
"""

Generic_TextLine = """
Terrible customer service.
Really great transaction.
Great price.
"""

Category_CSV = """
column_data,column_label
"Terrible customer service.","negative"
"Really great transaction.","positive"
"Great price.","positive"
"""

Category_fastText = """
__label__negative Terrible customer service.
__label__positive Really great transaction.
__label__positive Great price.
"""

Category_JSON = """
[
    {
        "column_data": "Terrible customer service.",
        "column_label": ["negative"]
    }
]
"""

Category_JSONL = """
{"column_data": "Terrible customer service.", "column_label": ["negative"]}
{"column_data": "Really great transaction.", "column_label": ["positive"]}
{"column_data": "Great price.", "column_label": ["positive"]}
"""

Text_CSV = """
column_data,column_label
"Hello!","こんにちは！"
"Good morning.","おはようございます。"
"See you.","さようなら。"
"""

Text_JSON = """
[
    {
        "text": "Hello!",
        "labels": ["こんにちは！"]
    }
]
"""

Text_JSONL = """
{"column_data": "Hello!", "column_label": ["こんにちは！"]}
{"column_data": "Good morning.", "column_label": ["おはようございます。"]}
{"column_data": "See you.", "column_label": ["さようなら。"]}
"""

Offset_JSONL = """
{"column_data": "EU rejects German call to boycott British lamb.", "column_label": [ [0, 2, "ORG"], ... ]}
{"column_data": "Peter Blackburn", "column_label": [ [0, 15, "PERSON"] ]}
{"column_data": "President Obama", "column_label": [ [10, 15, "PERSON"] ]}
"""

Offset_CoNLL = """
EU  B-ORG
rejects O
German  B-MISC
call  O
to  O
boycott O
British B-MISC
lamb  O
. O

Peter B-PER
Blackburn I-PER
"""
