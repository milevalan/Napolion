"""Utility functions and scripts used in various Modules"""
import re


def format_sent(sent_text):
    """Removes Extra whitespace in a sentence"""
    whitespaces = re.compile(r'\S+')
    return ' '.join(whitespaces.findall(sent_text)) + '\n'

