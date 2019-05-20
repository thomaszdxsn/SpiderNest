"""
author: thomaszdxsn
"""
import re

__all__ = ('RE_DATETIME', 'RE_IMG_SRC', 'RE_DATE', 'RE_UNIT_NUM', 'RE_CHINESE')


RE_DATETIME = re.compile(r'\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}')
RE_DATE = re.compile(r'\d{2,4}-\d{1,2}-\d{1,2}')
RE_IMG_SRC = re.compile(r'<img\s+src=[\'\"](.*?)[\'\"].*?/?>', flags=re.DOTALL|re.MULTILINE)
RE_UNIT_NUM = re.compile(r'([\d.]+)(万)?')
RE_CHINESE = re.compile(r'[\u4e00-\u9fa5]+')