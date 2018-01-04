import robozilla
from robozilla.decorators import skip_if_bug_open
from .data import cache_data

# MOCK BZ READER to avoid connection to bugzilla
from .base import BZReaderForTest
BZReaderForTest._cache_data = cache_data
robozilla.decorators.BZReader = BZReaderForTest


@skip_if_bug_open(
    'bugzilla',
    1377676,
    sat_version_picker=lambda: '6.2.9',
    config_picker=lambda: {'bz_credentials': {'user': '', 'password': ''}}
)
def test_closed_duplicate_runs():
    """
    1377676 is closed as DUPLICATE
    the duplicate BZ is also a DUPLICATE of another
    the final BZ in the chain is CLOSED ERRATA
    so the test runs
    """
    assert 1 == 1


@skip_if_bug_open(
    'bugzilla',
    8888888,
    sat_version_picker=lambda: '6.2.9',
    config_picker=lambda: {'bz_credentials': {'user': '', 'password': ''}}
)
def test_closed_duplicate_with_opened_dupe_never_run():
    """
    Bz 8888888 is flagged for 6.2.z + CLOSED DUPLICATE
    but it is DUPLICATE of 7777777
    which is flagged for 6.2.z +
    and is ASSIGNED so..
    This test should be SKIPPED as version here is 6.2.9
    """
    assert 1 == 2
