import re


def do_preprocessing(text: str):
    def _strip_multiple_whitespaces(s):
        re_whitespace = re.compile(r"(\s)+", re.UNICODE)
        return re_whitespace.sub(" ", s)

    pipeline = [
        _strip_multiple_whitespaces,
        str.strip,
    ]
    for filter in pipeline:
        text = filter(text)

    return text
