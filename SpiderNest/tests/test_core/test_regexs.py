"""
author: thomaszdxsn
"""
import pytest

from ...core.regexs import RE_DATE, RE_DATETIME, RE_IMG_SRC


@pytest.mark.parametrize('input,expect', [
    ('19-1-2', True),
    ('19-1-03', True),
    ('19-01-4', True),
    ('19-01-05', True),
    ('2019-1-2', True),
    ('2019-1-03', True),
    ('2019-01-4', True),
    ('2019-01-05', True),
])
def test_re_date(input, expect):
    match = RE_DATE.match(input) is not None
    assert match == expect


@pytest.mark.parametrize('input,expect', [
    ('19-1-2 00:01:02', True),
    ('19-1-03 02:01:3', True),
    ('19-01-4 01:2:3', True),
    ('19-01-05 1:2:3', True),
    ('2019-1-2 1:2', False),
    ('2019-1-03 1:02', False),
    ('2019-01-4 01:02', False),
    ('2019-01-05 01:2', False),
])
def test_re_datetime(input, expect):
    match = RE_DATETIME.match(input) is not None
    assert match == expect


@pytest.mark.parametrize('input,expect', [
    ('<img src="./a.jpg" asdfssdfsdf/>', True),
    ('<img src=\'./b.jpg\' asdfsdf/>', True),
    ('<a src="c.jpg" />', False),

])
def test_re_img_src(input, expect):
    match = RE_IMG_SRC.match(input) is not None
    assert match == expect