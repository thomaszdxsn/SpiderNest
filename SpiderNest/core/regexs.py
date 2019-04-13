"""
author: thomaszdxsn
"""
import re

__all__ = ('RE_DATETIME', 'RE_IMG_SRC')


RE_DATETIME = re.compile(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}')
RE_IMG_SRC = re.compile(r'src=[\'\"](.*?)[\'\"]', flags=re.DOTALL|re.MULTILINE)