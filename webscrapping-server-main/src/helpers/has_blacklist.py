import re

def has_blacklist(text, blacklist):
    try:
        if (not text or not isinstance(text, str) or not blacklist or not isinstance(blacklist, str)):
            return False

        blacklist_words = filter(lambda t: t != '', map(lambda t: t.strip(), blacklist.split(',')))
        words_regex = []

        for word in blacklist_words:
            word_regex = (r'').join(map(lambda t: t + "(s|es)?", filter(lambda t: t != '', word.split(' '))))

            if (re.search(r"\b{}\b".format(word_regex), text.lower())):
                return True
    except Exception as e:
        print(e)

    return False