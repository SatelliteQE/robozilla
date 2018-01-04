# coding: utf-8
import inspect
import logging
import os
import re
from functools import partial, wraps
from itertools import chain

import pytest
import requests
import unittest2

from robozilla.bz import BZReader
from robozilla.constants import (
    BUGZILLA_ENVIRON_SAT_VERSION,
    BUGZILLA_ENVIRON_USER_NAME,
    BUGZILLA_ENVIRON_USER_PASSWORD_NAME,
    BZ_OPEN_STATUSES,
    REDMINE_URL
)

LOGGER = logging.getLogger(__name__)

# A dict mapping bug IDs to python-bugzilla bug objects.
_bugzilla = {}

# A cache used by redmine-related functions.
#
# * _redmine['closed_statuses'] is used by `_redmine_closed_issue_statuses`
# * _redmine['issues'] is used by `skip_if_rm_bug_open`
#
_redmine = {
    'closed_statuses': None,
    'issues': {},
}


# FIXME: It would be better to collect a list of statuses which indicate an
# issue is open. Doing so would make the implementation of `wrapper` (in
# `skip_if_rm_bug_open`) simpler.
def _redmine_closed_issue_statuses():
    """Return a list of issue status IDs which indicate an issue is closed.

    This list of issue status IDs is not hard-coded. Instead, the Redmine
    server is consulted when generating this list.

    :return: Statuses which indicate an issue is closed.
    :rtype: list

    """
    # Is the list of closed statuses cached?
    if _redmine['closed_statuses'] is None:
        result = requests.get('%s/issue_statuses.json' % REDMINE_URL).json()
        # We've got a list of *all* statuses. Let's throw only *closed*
        # statuses in the cache.
        _redmine['closed_statuses'] = []
        for issue_status in result['issue_statuses']:
            if issue_status.get('is_closed', False):
                _redmine['closed_statuses'].append(issue_status['id'])

    return _redmine['closed_statuses']


def get_func_name(func, class_name=None):
    """Given a func object return standardized name to use across project"""
    names = [func.__module__]
    if class_name:
        names.append(class_name)
    names.append(func.__name__)
    return '.'.join(names)


class BugFetchError(Exception):
    """Indicates an error occurred while fetching information about a bug."""


def _get_redmine_bug_status_id(bug_id):
    """Fetch bug ``bug_id``.

    :param int bug_id: The ID of a bug in the Redmine database.
    :return: The status ID of that bug.
    :raises BugFetchError: If an error occurs while fetching the bug. For
        example, a network timeout occurs or the bug does not exist.

    """
    if bug_id in _redmine['issues']:
        LOGGER.debug('Redmine bug {0} found in cache.'.format(bug_id))
    else:
        # Get info about bug.
        LOGGER.info('Redmine bug {0} not in cache. Fetching.'.format(bug_id))
        result = requests.get(
            '{0}/issues/{1}.json'.format(REDMINE_URL, bug_id)
        )
        if result.status_code != 200:
            raise BugFetchError(
                'Redmine bug {0} does not exist'.format(bug_id)
            )
        result = result.json()

        # Place bug into cache.
        try:
            _redmine['issues'][bug_id] = result['issue']['status']['id']
        except KeyError as err:
            raise BugFetchError(
                'Could not get status ID of Redmine bug {0}. Error: {1}'
                .format(bug_id, err)
            )

    return _redmine['issues'][bug_id]


def rm_bug_is_open(bug_id, sat_version_picker=None,
                   config_picker=None):
    """Tell whether Redmine bug ``bug_id`` is open.

    If information about bug ``bug_id`` cannot be fetched, the bug is assumed
    to be closed.

    :param bug_id: The ID of the bug being inspected.
    :param sat_version_picker: not used, kept for API compatibility
    :param config_picker: not used, kept for API compatibility
    :return: ``True`` if the bug is open. ``False`` otherwise.
    :rtype: bool

    """
    status_id = None
    try:
        status_id = _get_redmine_bug_status_id(bug_id)
    except BugFetchError as err:
        LOGGER.warning(err)
    if status_id is None or status_id in _redmine_closed_issue_statuses():
        return False
    return True


def _extract_version(regular_exp, possible_version):
    """Extract version using regular_exp against possible_version string.
    Returns None if extraction is not possible
    arguments defaults to None for backwards compatibility
    :param regular_exp: A `re.compile` instance
    :param possible_version: The string in the form sat-x.x.x or x.x.x
    """
    try:
        # EAFP to get a float direct from `6.1` like strings before regexing
        return float(possible_version.strip())
    except ValueError:
        result = regular_exp.search(possible_version)
        if result:
            return float(result.group('version'))


# To get specifically the .z version as in sat-6.2.z
_to_zstream_version = partial(
    _extract_version, re.compile(r'sat-(?P<version>\d\.\d)\.z'))

# To get specifically versions as in sat-6.2.3
_to_downstream_version = partial(
    _extract_version, re.compile(r'sat-(?P<version>\d\.\d)\.\d'))

# to get untagged as in 6.2.9
_to_target_milestone_version = partial(
    _extract_version, re.compile(r'(?P<version>\d\.\d)\.\d'))

# match any version as in `sat-6.2.x` or `sat-6.2.0` or `6.2.9`
# will all result in `float(6.2)`
_to_float_version = partial(
    _extract_version, re.compile(r'(?:sat-)*?(?P<version>\d\.\d)\.\w*'))


def _skip_downstream_condition(bug, sat_version_picker=None):
    """Analyze bugzilla flags returning False if host version is greater or
    equal to min positive flag version, True otherwise.
    The `sat_version_picker` param should be a callable with no arguments
    which returns the sat version as string in format `x.y.z'

    :param flags: list
    :param sat_version_picker: callable
    :return: bool
    """
    flags = bug.get('flags', {})
    positive_flags = [k for k, v in flags.items() if v == '+']
    zstream_versions = list(filter(
        lambda version: version is not None,
        map(_to_zstream_version, positive_flags)
    ))
    downstream_versions = list(filter(
        lambda version: version is not None,
        map(_to_downstream_version, positive_flags)
    ))

    if len(downstream_versions) == 0 and len(zstream_versions) == 0:
        return True
    target_milestone_version = bug['target_milestone']

    has_down_and_zstream = downstream_versions and zstream_versions
    if has_down_and_zstream and target_milestone_version is 'Unspecified':
        LOGGER.warning('Bugzilla with both downstream and zstream flags and '
                       'unspecified target_milestone: {}'.format(bug))
        return True

    flag_version = _to_target_milestone_version(target_milestone_version)

    if flag_version is None or not has_down_and_zstream:
        if downstream_versions:
            flag_version = min(downstream_versions)
        else:
            flag_version = min(zstream_versions)

    try:
        sat_version = float(sat_version_picker())
    except (ValueError, TypeError):
        return False
    else:
        return sat_version < flag_version


def _check_skip_condition_for_one_bug(bug, consider_flags,
                                      sat_version_picker=None,
                                      config=None):
    """Check bug skip conditions. It will not take into account bug's flags
    if consider_flags parameter is False
    The `sat_version_picker` param should be a callable with no arguments
    which returns the sat version as string in format `x.y.z'
    The `config` param must be a dict storing a `upstream` key holding a
    boolean telling weather the system is upstream installation

    :param bug: bug to analyse conditions
    :param sat_version_picker: callable returning 'x.y.z'
    :param config: dict
    :return: boolean indicating if it must be skipped or not
    """
    config = config or {}
    # NEW, ASSIGNED, MODIFIED, POST
    if bug['status'] in BZ_OPEN_STATUSES:
        return True
    # elif bug.get('status_resolution', bug['status']) in BZ_CLOSED_STATUSES:
    #     return False
    elif config.get('upstream'):
        return False

    def skip_upstream_conditions():
        """do not test bugs with whiteboard 'verified in upstream' in
        downstream until they are in 'CLOSED' state
         Verify all conditions are True, stopping evaluation when
         first condition is False
        """
        yield bug['status'] != 'CLOSED'
        whiteboard = bug.get('whiteboard', '')
        yield whiteboard
        yield 'verified in upstream' in whiteboard.lower()

    return (all(skip_upstream_conditions()) or
            (consider_flags and _skip_downstream_condition(
                bug, sat_version_picker)))


def _check_skip_conditions_for_bug_and_clones(bug, consider_flags=True,
                                              sat_version_picker=None,
                                              config=None):
    """Check bug skip conditions for the bug and it's clones. If any of them
    returns False, test will not be skipped.
    Check flowchart: https://www.lucidchart.com/invitations/accept/
    3a595f1d-103f-49aa-99bf-ba1acb632b99
    The `sat_version_picker` param should be a callable with no arguments
    which returns the sat version as string in format `x.y.z'
    The `config` is a dict optionally containing keys:
        upstream|bz_credentials|wontfix_lookup

    :param bug: bug to analyse conditions
    :param sat_version_picker: callable retuning string 'x.y.z'
    :param config: dict
    :return: boolean indicating if it must be skipped or not

    """

    config = config or {}
    if bug is None:
        return False

    if bug.get('resolution') == 'DUPLICATE' and bug.get('duplicate_of') is not None:  # noqa
        # if is a DUPLICATE, unconsider the BZ and look only for the DUP and its clones  # noqa
        all_open = _check_skip_conditions_for_bug_and_clones(
            bug.get('duplicate_of'),
            consider_flags=consider_flags,
            sat_version_picker=sat_version_picker,
            config=config
        )
    else:
        # If not DUPLICATE then look to all clones and chain results
        all_bugs = chain([bug], bug.get('other_clones', {}).values())
        # If BZ was fixed in zstream of previous sat version it doesn't
        # necessarily mean it was ported to future sat version immediately,
        # thus we shouldn't rely on such closed BZ;
        # filter out clones for previous versions if there's a clone for the
        # same version as satellite
        filtered_bugs = list(all_bugs)
        if (
                len(filtered_bugs) > 1
                and sat_version_picker is not None
                and sat_version_picker() is not None
                and (not config or not config.get('upstream'))):

            def get_bug_versions(bug):
                """Form a set of satellite versions affected by BZ"""
                flags = bug.get('flags', {})
                positive_flags = [k for k, v in flags.items() if v == '+']
                zstream_versions = list(filter(
                    lambda version: version is not None,
                    map(_to_zstream_version, positive_flags)
                ))
                downstream_versions = list(filter(
                    lambda version: version is not None,
                    map(_to_downstream_version, positive_flags)
                ))
                return set(zstream_versions + downstream_versions)

            affected_clone_present = any(
                _to_float_version(sat_version_picker())
                in get_bug_versions(bug_or_clone)
                for bug_or_clone in filtered_bugs
            )
            if affected_clone_present:
                # remove not actual bugs from list
                filtered_bugs = [
                    bug_or_clone for bug_or_clone in filtered_bugs
                    if _to_float_version(sat_version_picker())
                    in get_bug_versions(bug_or_clone)
                ]

        skip_results = (
            _check_skip_condition_for_one_bug(
                bug_or_clone, consider_flags, sat_version_picker, config
            )
            for bug_or_clone in filtered_bugs
        )
        all_open = all(skip_results)

    if all_open:
        LOGGER.debug('Bugzilla {0} is open'.format(bug.get('id')))

    return all_open


class BZUnauthenticatedCall(Exception):
    """Indicates unauthenticated call was made into Bugzilla API"""

    def __init__(self, bug, *args, **kwargs):
        """Unauthenticated calls can be done but will not retrieve flag info.
        So basic bug data can still be checked and that is the reason a bug
        must be provided as parameter so one handling this exceptions can
        still have access to it

        :param bug: bug returned on API call
        :param args: args to be passed to Exception __init__ method
        :param kwargs: kwargs to be passed to Exception __init__ method
        """
        super(BZUnauthenticatedCall, self).__init__(*args, **kwargs)
        self.bug = bug


def _get_bugzilla_bug(bug_id, bz_credentials=None):
    """Fetch bug ``bug_id``.

    :param int bug_id: The ID of a bug in the Bugzilla database.
    :param bz_credentials: must be a dict with user and password.
    :return: A FRIGGIN UNDOCUMENTED python-bugzilla THING.
    :raises BugFetchError: If an error occurs while fetching the bug. For
        example, a network timeout occurs or the bug does not exist.

    """
    # Is bug ``bug_id`` in the cache?
    if bug_id in _bugzilla:
        LOGGER.debug('Bugzilla bug {0} found in cache.'.format(bug_id))
    else:
        LOGGER.info('Bugzilla bug {0} not in cache. Fetching.'.format(bug_id))
        # Make a network connection to the Bugzilla server.
        bz_credentials = bz_credentials or {}

        reader = BZReader(
            bz_credentials,
            include_fields=[
                'id', 'status', 'whiteboard', 'flags', 'resolution',
                'target_milestone'
            ],
            follow_clones=True,
            follow_duplicates=True  # only when resolution is 'DUPLICATE'
        )
        _bugzilla[bug_id] = reader.get_bug_data(bug_id)
        if not bz_credentials:
            raise BZUnauthenticatedCall(
                _bugzilla[bug_id],
                'Unauthenticated call made to BZ API, no flags data will '
                'be available'
            )

    return _bugzilla[bug_id]


def bz_bug_is_open(bug_id, sat_version_picker=None,
                   config_picker=None):
    """Tell whether Bugzilla bug ``bug_id`` is open.

    If information about bug ``bug_id`` cannot be fetched, the bug is assumed
    to be closed.

    Example call:

        bz_bug_is_open(
            1079482,
            sat_version_picker=lambda: '6.2.10',
            config_picker=lambda: {
                'bz_credentials': {'user': '', 'password': ''}
            }
        )

    Or make it a partial function:

        from functools import partial
        bz_bug_is_open = partial(
            bz_bug_is_open,
            sat_version_picker=a_function_returning_version,
            config_picker=a_function_returning_config_dict
        )

    And then use as usual:

        bz_bug_is_open(1079482)

    :param bug_id: The ID of the bug being inspected.
    :param sat_version_picker: a callable returning 'x.y.z'
    :param config_picker: a callable returning a dictionary optionally with
        {'bz_credentials': {'user': '', 'password': ''}}
    :return: ``True`` if the bug is open. ``False`` otherwise.
    :rtype: bool

    """
    config_picker = config_picker or default_config_picker
    sat_version_picker = sat_version_picker or default_version_picker

    config = config_picker() if callable(config_picker) else {}
    bz_credentials = config.get('bz_credentials')

    try:
        bug = _get_bugzilla_bug(bug_id, bz_credentials=bz_credentials)
    except BZUnauthenticatedCall as err:
        LOGGER.warning(err)
        return _check_skip_conditions_for_bug_and_clones(
            err.bug, False,
            sat_version_picker=sat_version_picker, config=config
        )
    else:
        return _check_skip_conditions_for_bug_and_clones(
            bug, sat_version_picker=sat_version_picker, config=config
        )


class BugTypeError(Exception):
    """Indicates that an incorrect bug type was specified."""


class skip_if_bug_open(object):  # noqa pylint:disable=C0103,R0903
    """A decorator that can be used to skip a unit test.
    Example:

        @skip_if_bug_open(
            'bugzilla', 1079482,
            sat_version_picker=lambda: '6.2.10',
            config_picker=lambda: {
                'bz_credentials': {'user': '', 'password': ''}
            }
        )
        def test_something():
            assert ....

    Or make it a partial function:

        from functools import partial
        skip_if_bug_open = partial(
            skip_if_bug_open,
            sat_version_picker=a_function_returning_version,
            config_picker=a_function_returning_config_dict
        )

    Then use as usual:

        @skip_if_bug_open('bugzilla', 1079482)
        def test():
            ...
    """

    def __init__(self, bug_type, bug_id, sat_version_picker=None,
                 config_picker=None):
        """Record decorator arguments.

        :param str bug_type: Either 'bugzilla' or 'redmine'.
        :param sat_version_picker: a callable returning 'x.y.z'
        :param config_picker: a callable returning a dictionary optionally with
            {'bz_credentials': {'user': '', 'password': ''}}
        :param int bug_id: The ID of the bug to check when the decorator is
            run.

        """
        # Define first from which class the decorator has been called
        # we need this to make a naming deference between tests that are
        # located at module level and those in diffrent TestCases
        # we need to use inspect as the function has been wrapped and lost many
        # of it's original attributes
        self.caller_class_name = None
        class_names = []
        class_name = None
        index = 1
        current_frame = inspect.currentframe()
        while class_name != '<module>' and index <= 3:
            if class_name and class_name != 'decorator':
                class_names.append(class_name)
            class_name = inspect.getouterframes(current_frame)[index][3]
            index += 1
        class_names.reverse()
        if class_names:
            self.caller_class_name = class_names[0]
        self.bug_type = bug_type
        self.bug_id = bug_id
        self.sat_version_picker = sat_version_picker
        self.config_picker = config_picker

    def __call__(self, func):
        """Define and return a replacement for ``func``.

        :param func: The function being decorated.

        """
        self.register_bug_id(func)

        if self.bug_type not in ('bugzilla', 'redmine'):
            raise BugTypeError(
                '"{0}" is not a recognized bug type. Did you mean '
                '"bugzilla" or "redmine"?'.format(self.bug_type)
            )

        @wraps(func)
        def wrapper_func(*args, **kwargs):
            """Run ``func`` or skip it by raising an exception.

            If information about bug ``bug_id`` can be fetched and the bug is
            open, skip test ``func``. Otherwise, run the test.

            :return: The return value of test method ``func``.
            :raises unittest2.SkipTest: If bug ``bug_id`` is open.
            :raises BugTypeError: If ``bug_type`` is not recognized.

            """
            if self.bug_type == 'bugzilla' and bz_bug_is_open(
                        self.bug_id,
                        sat_version_picker=self.sat_version_picker,
                        config_picker=self.config_picker
                    ):
                LOGGER.debug(
                    'Skipping test %s in module %s due to Bugzilla bug #%s',
                    func.__name__,
                    func.__module__,
                    self.bug_id
                )
                raise unittest2.SkipTest(
                    'Skipping test due to open Bugzilla bug #{0}.'
                    ''.format(self.bug_id)
                )
            if self.bug_type == 'redmine' and rm_bug_is_open(self.bug_id):
                LOGGER.debug(
                    'Skipping test %s in module %s due to Redmine bug #%s',
                    func.__name__,
                    func.__module__,
                    self.bug_id
                )
                raise unittest2.SkipTest(
                    'Skipping test due to open Redmine bug #{0}.'
                    ''.format(self.bug_id)
                )
            # Run the test method.
            return func(*args, **kwargs)

        # This function replaces what is being decorated.
        return wrapper_func

    def register_bug_id(self, func):  # pragma: no cover
        """Every time the test is decorated, takes the BZ number and
        register it in pytest global namespace variable to be accessible in
        conftest in order to perform the filtering of test collection
        if settings.bugzilla.wontfix_lookup == False just returns False.
        This only runs if `bugzilla` exists in pytest namespace
        """
        bz_namespace = getattr(pytest, 'bugzilla', None)
        if bz_namespace:
            conf = self.config_picker() if callable(self.config_picker) else {}
            if conf.get('wontfix_lookup') is True:
                bz_namespace.decorated_functions.append(
                    (
                        get_func_name(func, class_name=self.caller_class_name),
                        str(self.bug_id)
                    )
                )


def pytest_skip_if_bug_open(bug_type, bug_id, sat_version_picker=None,
                            config_picker=None):
    """Pytest parametrized tests can't work with the default `skip_if_bug_open`
    this decorator returns a Pytest.mark which can work with that scenario.

    Example:

        @pytest_skip_if_bug_open(
            'bugzilla', 1079482,
            sat_version_picker=lambda: '6.2.10',
            config_picker=lambda: {
                'bz_credentials': {'user': '', 'password': ''}
            }
        )
        @pytest.mark.parametrize("foo,bar", [('1', '2')], ids=['foo and bar'])
        def test_something(foo, bar):
            assert ....

    Or make it a partial function:

        from functools import partial
        pytest_skip_if_bug_open = partial(
            pytest_skip_if_bug_open,
            sat_version_picker=a_function_returning_version,
            config_picker=a_function_returning_config_dict
        )

    Then use as usual:

        @pytest_skip_if_bug_open('bugzilla', 1079482)
        @pytest.mark.parametrize("foo,bar", [('1', '2')], ids=['foo and bar'])
        def test(foo, bar):
            ...

    :param str bug_type: Either 'bugzilla' or 'redmine'.
    :param int bug_id: The ID of the bug to check when the decorator isrun.
    :param sat_version_picker: a callable returning 'x.y.z'
    :param config_picker: a callable returning a dictionary optionally with
        {'bz_credentials': {'user': '', 'password': ''}}

    """
    return pytest.mark.skipif(
        (bz_bug_is_open if bug_type == 'bugzilla' else rm_bug_is_open)(
            bug_id, sat_version_picker, config_picker
        ),
        reason='Skipping due to {0} {1}'.format(bug_type, bug_id)
    )


def default_config_picker():
    """If a custom config picker is not provided this one will be used by
    default getting credentials from environment variables:
        BUGZILLA_USER_NAME and BUGZILLA_USER_PASSWORD
    """
    user = os.environ.get(BUGZILLA_ENVIRON_USER_NAME)
    password = os.environ.get(BUGZILLA_ENVIRON_USER_PASSWORD_NAME)
    if user or password:
        return {'bz_credentials': {'user': user, 'password': password}}
    return {}


def default_version_picker():
    """If a version picker is not provided this one is used getting the
    varsion from environment variable:
        BUGZILLA_SAT_VERSION
    """
    return os.environ.get(BUGZILLA_ENVIRON_SAT_VERSION) or None
