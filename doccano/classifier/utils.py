"""
Utilities.
"""
import json


def train_test_split(data):
    x_train, x_test, y_train, ids = [], [], [], []
    for d in data:
        text = d['text']
        label = d['label']
        if d['manual']:
            x_train.append(text)
            y_train.append(label)
        else:
            x_test.append(text)
            ids.append(d['id'])

    return x_train, x_test, y_train, ids


def load_dataset(filename):
    with open(filename) as f:
        data = [json.loads(line) for line in f]

    return data


def save_dataset(obj, filename):
    with open(filename, 'w') as f:
        for line in obj:
            f.write('{}\n'.format(json.dumps(line)))
