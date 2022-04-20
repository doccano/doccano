CATEGORY_CSV = """
text,label
"Terrible customer service.","negative"
"Really great transaction.","positive"
"Great price.","positive"
"""

CATEGORY_FASTTEXT = """
__label__negative Terrible customer service.
__label__positive Really great transaction.
__label__positive Great price.
"""

CATEGORY_JSON = """
[
    {
        "text": "Terrible customer service.",
        "label": ["negative"]
    }
]
"""

CATEGORY_JSONL = """
{"text": "Terrible customer service.", "label": ["negative"]}
{"text": "Really great transaction.", "label": ["positive"]}
{"text": "Great price.", "label": ["positive"]}
"""

TEXT_CSV = """
text,label
"Hello!","こんにちは！"
"Good morning.","おはようございます。"
"See you.","さようなら。"
"""

TEXT_JSON = """
[
    {
        "text": "Hello!",
        "label": ["こんにちは！"]
    }
]
"""

TEXT_JSONL = """
{"text": "Hello!", "label": ["こんにちは！"]}
{"text": "Good morning.", "label": ["おはようございます。"]}
{"text": "See you.", "label": ["さようなら。"]}
"""

SPAN_JSONL = """
{"text": "EU rejects German call to boycott British lamb.", "label": [ [0, 2, "ORG"], [11, 17, "MISC"], ... ]}
{"text": "Peter Blackburn", "label": [ [0, 15, "PERSON"] ]}
{"text": "President Obama", "label": [ [10, 15, "PERSON"] ]}
"""

ENTITY_AND_RELATION_JSONL = """
{
    "text": "Google was founded on September 4, 1998, by Larry Page and Sergey Brin.",
    "entities": [
        {
            "id": 0,
            "start_offset": 0,
            "end_offset": 6,
            "label": "ORG"
        },
        {
            "id": 1,
            "start_offset": 22,
            "end_offset": 39,
            "label": "DATE"
        },
        {
            "id": 2,
            "start_offset": 44,
            "end_offset": 54,
            "label": "PERSON"
        },
        {
            "id": 3,
            "start_offset": 59,
            "end_offset": 70,
            "label": "PERSON"
        }
    ],
    "relations": [
        {
            "id": 0,
            "from_id": 0,
            "to_id": 1,
            "type": "foundedAt"
        },
        {
            "id": 1,
            "from_id": 0,
            "to_id": 2,
            "type": "foundedBy"
        },
        {
            "id": 2,
            "from_id": 0,
            "to_id": 3,
            "type": "foundedBy"
        }
    ]
}
"""

CATEGORY_IMAGE_CLASSIFICATION = """
[
    {
        "filename": "20210514.png",
        "label": ["cat"]
    }
]
"""

SPEECH_TO_TEXT = """
[
    {
        "filename": "20210514.mp3",
        "label": ["Lorem ipsum dolor sit amet"]
    }
]
"""

INTENT_JSONL = """
{"text": "Find a flight from Memphis to Tacoma", "entities": [[0, 26, "City"], [30, 36, "City"]], "cats": ["flight"]}
{"text": "I want to know what airports are in Los Angeles", "entities": [[36, 47, "City"]], "cats": ["airport"]}
"""
