import string

def get_key_choices():
    selectKey, shortKey = [c for c in string.ascii_lowercase], [c for c in string.ascii_lowercase]
    checkKey = 'ctrl shift'
    shortKey += [ck + ' ' + sk for ck in checkKey.split() for sk in selectKey]
    shortKey += [checkKey + ' ' + sk for sk in selectKey]
    shortKey += ['']
    KEY_CHOICES = ((u, c) for u, c in zip(shortKey, shortKey))
    return KEY_CHOICES
