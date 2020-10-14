import html
import re

def replace_string_with_pattern(data,pattern,replace_with):
    if not isinstance(data, str):
        return data
    return re.sub(pattern,replace_with, data)

def clear_empty_string(string):
    return string if string != ' ' else None

def decode_html_chars(data):
    if not isinstance(data, str):
        return data
    return html.unescape(data)
