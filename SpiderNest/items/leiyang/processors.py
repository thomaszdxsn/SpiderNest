"""
author: thomaszdxsn
"""
import re
from datetime import datetime
from urllib.parse import urljoin
from typing import Union, List

import arrow
from arrow.parser import ParserError

__all__ = ('created_time_input_processor', 'Exists', 'populate_abs_url')

_CREATED_TIME_REG_MINS_AGO = re.compile(r'(\d{1,2})\s分钟前', flags=re.U)
_CREATED_TIME_REG_HOUR_AGO = re.compile(r'(\d{1,2})\s小时前', flags=re.U)
_CREATED_TIME_REG_DAY_AGO = re.compile(r'(\d{1,2})\s天前', flags=re.U)
_CREATED_TIME_REG_YESTERDAY = re.compile(r'昨天\s(\d{1,2}:\d{1,2})', flags=re.U)
_CREATED_TIME_REG_DAY_BEFORE_YESTERDAY = re.compile(r'前天\s(\d{1,2}:\d{1,2})', flags=re.U)
_CREATED_TIME_HALF_HOUR_AGO = re.compile(r'半小时前', flags=re.U)


def _created_time_input_processor(val: str) -> arrow.Arrow:
    try:
        return arrow.get(val).replace(tzinfo='Asia/Shanghai')
    except ParserError:
        match = _CREATED_TIME_REG_MINS_AGO.match(val)
        if match:
            minutes = int(match.group(1))
            return arrow.now().shift(minutes=-minutes)

        match = _CREATED_TIME_REG_HOUR_AGO.match(val)
        if match:
            hours = int(match.group(1))
            return arrow.now().shift(hours=-hours)

        match = _CREATED_TIME_REG_DAY_AGO.match(val)
        if match:
            days = int(match.group(1))
            return arrow.now().shift(days=-days)

        match = _CREATED_TIME_REG_YESTERDAY.match(val)
        if match:
            yesterday = format(arrow.now().shift(days=-1).datetime, '%Y-%m-%d')
            return arrow.get('{} {}'.format(yesterday, match.group(1)))

        match = _CREATED_TIME_REG_DAY_BEFORE_YESTERDAY.match(val)
        if match:
            day_before_yesterday = format(arrow.now().shift(days=-2).datetime, '%Y-%m-%d')
            return arrow.get('{} {}'.format(day_before_yesterday, match.group(1)))

        match = _CREATED_TIME_HALF_HOUR_AGO.match(val)
        if match:
            return arrow.now().shift(minutes=-30)
    return arrow.get(
        val, ['YYYY-M-DD HH:mm:ss', 'YYYY-MM-D HH:mm:ss', 'YYYY-M-D HH:mm:ss']
    ).replace(tzinfo='Asia/Shanghai')


def strip_datetime_fields(dt: Union[arrow.Arrow, datetime], fields: List[str]) -> datetime:
    result = dt.replace(**{field: 0 for field in fields})
    if isinstance(result, arrow.Arrow):
        return result.datetime
    return result


def created_time_input_processor(val: str) -> datetime:
    dt = _created_time_input_processor(val)
    return strip_datetime_fields(dt, ['second', 'microsecond'])


def populate_abs_url(url, loader_context):
    if url.startswith('http'):
        return url
    return urljoin(loader_context['base_url'], url)


class Exists(object):

    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return True
        return False