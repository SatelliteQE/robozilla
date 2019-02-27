import os
import json

import click

from robozilla.parser import Parser
from robozilla.constants import (
    BUGZILLA_ENVIRON_USER_NAME,
    BUGZILLA_ENVIRON_USER_PASSWORD_NAME,
    BUGZILLA_QUERY_PRODUCT,
    DEFAULT_INCLUDE_FIELDS,
    COVERAGE_AUTOMATED,
    COVERAGE_BACKLOG,
    COVERAGE_INCLUDE_FIELDS,
    COVERAGE_REJECTED,
)
from robozilla.filters import get_filters
from robozilla.query.query import BZQuery
from robozilla.query.exp import decode_groups


@click.group()
def main():
    pass


@main.command(help='Scan robottelo code for bug usage')
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
def scan(scan_dir, filters, warn, all, duplicates, clones, depends, echo, user,
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


@main.command(help='The bugs qa_coverage discovery')
@click.option('-c', '--exclude-components', default=None,
              help='The components to exclude')
@click.option('-f', '--include-flags', default=None,
              help='The flags to include')
@click.option('-e', '--exclude-flags', default=None,
              help='The flags to exclude')
@click.option('--start-date', default=None,
              help='the change from date (chfieldfrom)')
@click.option('--end-date', default='Now',
              help='the change to date  (chfieldto), default value Now')
@click.option('--echo-only/--no-echo-only', default=False,
              help='the change to date  (chfieldto), default value Now')
@click.option('--user', default=None,
              help='The bugzilla user')
@click.option('--password', default=None,
              help='The bugzilla user password')
@click.option('--product', default=BUGZILLA_QUERY_PRODUCT,
              help='The bugzilla query product,'
                   ' default is "Red Hat Satellite 6"')
def coverage(exclude_components, include_flags, exclude_flags, start_date,
             end_date, echo_only, user, password, product):

    reader_options = {}
    if not user and BUGZILLA_ENVIRON_USER_NAME in os.environ:
        user = os.environ[BUGZILLA_ENVIRON_USER_NAME]

    if not password and BUGZILLA_ENVIRON_USER_PASSWORD_NAME in os.environ:
        password = os.environ[BUGZILLA_ENVIRON_USER_PASSWORD_NAME]
    if (user and not password) or (not user and password):
        raise Exception('you must provide a user and password')
    if user and password:
        reader_options['credentials'] = {'user': user,
                                         'password': password}
        click.echo('connecting to bugzilla as user: {}'.format(user),
                   color='green')
    else:
        click.echo('connecting to bugzilla without credentials', color='red')

    for coverage_type in [COVERAGE_REJECTED, COVERAGE_AUTOMATED,
                          COVERAGE_BACKLOG]:

        include_any = ''
        if include_flags:
            include_any = 'flag_name~[~]{}'.format(include_flags)

        include_all = 'flag_name={}'.format(coverage_type)
        if exclude_components:
            exclude_components_list = exclude_components.split(' ')
            for component_string in exclude_components_list:
                if component_string:
                    include_all = '{0},component!~~{1}'.format(
                        include_all, component_string)

        if exclude_flags:
            exclude_exp = 'flag_name![~]{0}'.format(exclude_flags)
            if include_all:
                include_all = '{0},{1}'.format(include_all, exclude_exp)
            else:
                include_all = exclude_exp

        kwargs = dict()
        kwargs['product'] = product
        kwargs['include_fields'] = COVERAGE_INCLUDE_FIELDS
        if start_date:
            kwargs['start_date'] = start_date
        if end_date:
            kwargs['end_date'] = end_date
        query = decode_groups(include_all=include_all, include_any=include_any,
                              **kwargs)

        if echo_only:
            click.echo('{}:'.format(coverage_type))
            click.echo('include_all:')
            click.echo(include_all)
            click.echo('include_any:')
            click.echo(include_any)
            click.echo(json.dumps(query, indent=4))
        else:

            bz_query = BZQuery(**reader_options)
            bugs = bz_query.query(**query)
            print("{} = {}".format(coverage_type, len(bugs)))


if __name__ == '__main__':
    main()
