def is_isbn_or_key(q):
    result = 'key'
    short_word = q.replace('-','')
    if len(q) ==13 and q.isdigit():
        result = 'isbn'
    elif '-' in q and len(short_word)==10 and short_word.isdigit():
        result = 'key'
    return result