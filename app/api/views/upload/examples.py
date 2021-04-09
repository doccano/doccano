Generic_TextFile = """
├── 202104210943.txt
├── 202104210944.txt
└── 202104210945.txt
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
{"text": "Hello!", "labels": ["こんにちは！"]}
{"text": "Good morning.", "labels": ["おはようございます。"]}
{"text": "See you.", "labels": ["さようなら。"]}
"""

Offset_JSONL = """
{"text": "EU rejects German call to boycott British lamb.", "labels": [ [0, 2, "ORG"], [11, 17, "MISC"], ... ]}
{"text": "Peter Blackburn", "labels": [ [0, 15, "PERSON"] ]}
{"text": "President Obama", "labels": [ [10, 15, "PERSON"] ]}
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
