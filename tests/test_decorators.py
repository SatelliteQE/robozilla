import pytest
import robozilla
from robozilla.decorators import pytest_skip_if_bug_open, skip_if_bug_open
from data import cache_data

# MOCK BZ READER to avoid connection to bugzilla
from base import BZReaderForTest
BZReaderForTest._cache_data = cache_data
robozilla.decorators.BZReader = BZReaderForTest


@pytest_skip_if_bug_open(
    'bugzilla',
    1461026,
    sat_version_picker=lambda: '6.2',
    config_picker=lambda: {'bz_credentials': {'user': 'foo@bar.com',
                                              'password': '1234'}}
)
@pytest.mark.parametrize("pre,post", [('1', '2'), ('1', '2')],
                         ids=['foo and bar', 'baz and gaz'])
def test_positive_cvs_by_repository_ids(pre, post):
    print('this should never run')
    assert pre == post  # 1 != 2


@skip_if_bug_open('bugzilla', 1461026)
def test_default_pickers():
    print('this should never run')
    assert 1 == 2


@pytest_skip_if_bug_open('bugzilla', 1461026)
def test_default_pickers_for_pytest():
    print('this should never run')
    assert 1 == 2
