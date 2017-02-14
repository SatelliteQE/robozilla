import os

import click

from robozilla.parser import Parser
from robozilla.constants import (
    BUGZILLA_ENVIRON_USER_NAME,
    BUGZILLA_ENVIRON_USER_PASSWORD_NAME,
    DEFAULT_INCLUDE_FIELDS,
)
from robozilla.filters import get_filters


@click.command()
@click.argument('scan_dir', default=None, required=0)
@click.option('--filters', default='all',
              help='The filter to use when scanning, default=all, available:'
                   ' all, decorator, function')
@click.option('--warn/--no-warn', default=True,
              help='Whether to output the warnings, default is warn')
@click.option('--all/--no-all', default=False,
              help='this to get all duplicates clones depends bug info,'
                   ' default is no-all')
@click.option('--duplicates/--no-duplicates', default=False,
              help='Whether to get duplicates of bug info,'
                   ' default is no-duplicates')
@click.option('--clones/--no-clones', default=False,
              help='Whether to get clones of bug info, default is no-clones')
@click.option('--depends/--no-depends', default=False,
              help='Whether to get depends on bug info, default is no-depends')
@click.option('--echo/--no-echo', default=True,
              help='Whether to echo entry parameters, default is echo')
@click.option('--user', default=None,
              help='The bugzilla user')
@click.option('--password', default=None,
              help='The bugzilla user password')
def main(scan_dir, filters, warn, all, duplicates, clones, depends, echo, user,
         password):

    if all:
        duplicates = True
        clones = True
        depends = True

    if scan_dir is None:
        scan_dir = os.path.realpath(os.path.curdir)

    if echo:
        click.echo('scanning: {}'.format(scan_dir))
        click.echo('warn: {}'.format(warn))
        click.echo('duplicates: {}'.format(duplicates))
        click.echo('clones: {}'.format(clones))
        click.echo('depends: {}'.format(depends))
        click.echo('filters: {}'.format(filters))

    filters = get_filters(filters)
    if not filters:
        raise ValueError('filter "{}" does not exit'.format(filters))

    reader_options = {
            'follow_clones': False,
            'follow_duplicates': False,
            'follow_depends': False,
            'include_fields': DEFAULT_INCLUDE_FIELDS
    }
    if clones:
        reader_options['follow_clones'] = True

    if duplicates:
        reader_options['follow_duplicates'] = True

    if depends:
        reader_options['follow_depends'] = True

    if not user and BUGZILLA_ENVIRON_USER_NAME in os.environ:
            user = os.environ[BUGZILLA_ENVIRON_USER_NAME]

    if not password and BUGZILLA_ENVIRON_USER_PASSWORD_NAME in os.environ:
            password = os.environ[BUGZILLA_ENVIRON_USER_PASSWORD_NAME]

    if (user and not password) or (not user and password):
        raise Exception('you must provide a user and password')
    if user and password:
        reader_options['credentials'] = {'user': user, 'password': password}
        click.echo('connecting to bugzilla as user: {}'.format(user))
    else:
        if echo:
            click.echo('connecting to bugzilla without credentials')

    parser = Parser(
        scan_dir,
        filters=filters,
        reporter=None,
        bz_reader=None,
        environment=None,
        reader_options=reader_options,
        warn=warn
    )
    parser.parse(report=True)


if __name__ == '__main__':
    main()
