Category_CSV = """
text,label
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
        "text": "Terrible customer service.",
        "label": ["negative"]
    }
]
"""

Category_JSONL = """
{"text": "Terrible customer service.", "label": ["negative"]}
{"text": "Really great transaction.", "label": ["positive"]}
{"text": "Great price.", "label": ["positive"]}
"""

Text_CSV = """
text,label
"Hello!","こんにちは！"
"Good morning.","おはようございます。"
"See you.","さようなら。"
"""

Text_JSON = """
[
    {
        "text": "Hello!",
        "label": ["こんにちは！"]
    }
]
"""

Text_JSONL = """
{"text": "Hello!", "label": ["こんにちは！"]}
{"text": "Good morning.", "label": ["おはようございます。"]}
{"text": "See you.", "label": ["さようなら。"]}
"""

Offset_JSONL = """
{"text": "EU rejects German call to boycott British lamb.", "label": [ [0, 2, "ORG"], [11, 17, "MISC"], ... ]}
{"text": "Peter Blackburn", "label": [ [0, 15, "PERSON"] ]}
{"text": "President Obama", "label": [ [10, 15, "PERSON"] ]}
"""

CategoryImageClassification = """
[
    {
        "filename": "20210514.png",
        "label": ["cat"]
    }
]
"""
