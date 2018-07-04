"""
Preprocessor.
"""
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer

t = MeCab.Tagger('-Owakati')


def tokenize(text):
    """Tokenize Japanese text.

    Args:
        text: Japanese string.

    Returns:
        A list of words.
    """
    words = t.parse(text).rstrip().split()

    return words


def build_vectorizer():
    vectorizer = TfidfVectorizer(tokenizer=tokenize)

    return vectorizer
