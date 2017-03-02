from __future__ import print_function

import os

import bugzilla

from robozilla.constants import (
    BUGZILLA_ENVIRON_USER_NAME,
    BUGZILLA_ENVIRON_USER_PASSWORD_NAME,
    BUGZILLA_QUERY_PRODUCT,
    BUGZILLA_URL,
)


def get_bug_status_flags_string(flags):
    flags_list = []
    for status_flag in flags:
        name = status_flag.get('name', '')
        value = status_flag.get('status', '')
        flags_list.append('{0}{1}'.format(name, value))
    return ', '.join(flags_list)


class BZQuery(object):

    def __init__(self, credentials=None):

        self._connection = None
        if credentials is None:
            credentials = {}

        if not credentials:
            if BUGZILLA_ENVIRON_USER_NAME in os.environ:
                credentials['user'] = os.environ[
                    BUGZILLA_ENVIRON_USER_NAME]

            if BUGZILLA_ENVIRON_USER_PASSWORD_NAME in os.environ:
                credentials['password'] = os.environ[
                    BUGZILLA_ENVIRON_USER_PASSWORD_NAME]

        self.credentials = credentials

    def _get_connection(self):
        if not self._connection:
            bz_conn = bugzilla.RHBugzilla(url=BUGZILLA_URL, **self.credentials)
            self._connection = bz_conn
        return self._connection

    def query(self, **kwargs):
        bz_conn = self._get_connection()
        bq_kwargs = {}
        if 'product' not in kwargs:
            bq_kwargs['product'] = BUGZILLA_QUERY_PRODUCT
        query = bz_conn.build_query(**bq_kwargs)
        query.update(kwargs)

        return bz_conn.query(query)
