import pytest
import robozilla
from robozilla.decorators import (
    pytest_skip_if_bug_open, skip_if_bug_open, bz_bug_is_open
)
from .data import cache_data

# MOCK BZ READER to avoid connection to bugzilla
from .base import BZReaderForTest
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


@skip_if_bug_open('bugzilla', 9999999)
def test_closed_runs():
    assert 2 == 2


@skip_if_bug_open('bugzilla', 5555555)
def test_closed_next_release_runs():
    assert 2 == 2


@skip_if_bug_open('bugzilla', 4444444)
def test_closed_not_a_bug_runs():
    assert 2 == 2


@skip_if_bug_open('bugzilla', 3333333)
def test_closed_worksforme_runs():
    assert 2 == 2


@skip_if_bug_open('bugzilla', 2222222)
def test_closed_errata_runs():
    assert 2 == 2


def test_all_open():
    open_bugs = [
        int(key) for key, val in cache_data.items()
        if val.get('status_resolution', val['status'])
        in robozilla.constants.BZ_OPEN_STATUSES
    ]
    for bug_id in open_bugs:
        assert bz_bug_is_open(bug_id) is True


def test_all_closed():
    closed_bugs = [
        int(key) for key, val in cache_data.items()
        if val.get('status_resolution', val['status'])
        in robozilla.constants.BZ_CLOSED_STATUSES
    ]
    for bug_id in closed_bugs:
        assert bz_bug_is_open(bug_id) is False
