import re


def is_link(input_string):
    pattern = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    return bool(pattern.match(input_string))


def is_youtube_link(input_string):
    pattern = re.compile(r"https://www.youtube.com/watch\?v=([a-zA-Z0-9_-]+)")
    return bool(pattern.match(input_string))
