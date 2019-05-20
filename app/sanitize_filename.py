def sanitize_filename(filename):
    return filename \
        .replace('"', '') \
        .replace('?', '') \
        .replace('/', '-') \
        .replace(' ', '_') \
        .lower() \
        .replace(':', '_') \
