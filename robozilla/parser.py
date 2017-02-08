
import time

import six

from robozilla.bz import BZReader
from robozilla.filters import BZDecorator, BZIsOpen
from robozilla.providers.fs import FilesProvider
from robozilla.reporters import RawReporter


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class Parser(object):

    def __init__(self, files_provider, filters=None, reporter=None, warn=True,
                 bz_reader=None, environment=None, reader_options=None):

        if isinstance(files_provider, six.string_types):
                files_provider = FilesProvider(files_provider)

        self.files_provider = files_provider
        self.filters = filters if filters is not None else [
            BZDecorator, BZIsOpen
        ]
        self.bz_reader = bz_reader or BZReader(**(reader_options or {}))
        self.reporter = reporter or RawReporter(
            bz_reader=bz_reader, environment=environment
        )
        self.warn = warn

    def _parse_file(self, file_path):
        with open(file_path) as fr:
            line_number = 0
            for line in fr:
                for filter_handler in self.filters:
                    bug_ids = filter_handler.retrieve(line)
                    if (not bug_ids and self.warn and
                            filter_handler.is_string_present(line)):
                        self.reporter.output_warn(
                            'WARNING: {0} handler string found, but no bug id'
                            ' retrieved'.format(filter_handler.name))
                        self.reporter.output_warn(
                            '   line : {0} file: {1}'.format(
                                line_number, file_path))
                        self.reporter.output_warn(
                            '   line content: {}'.format(line.strip()))

                    for bug_id in bug_ids:
                        yield (bug_id, file_path, line_number,
                               filter_handler.name)

                line_number += 1

    def parse(self, report=False, bulk=True, chunk_size=150):
        if report:
            bug_files_path = []
            files_data = {}
            self.reporter.start()

        occurrences_counter = 0
        bug_objects = {}
        for file_path in self.files_provider.get_files():
            for data in self._parse_file(file_path):
                bug_id, bug_file_path, line_number, handler_name = data
                occurrences_counter += 1
                bug_file_data = {
                    'file_path': bug_file_path,
                    'line_number': line_number,
                    'handler_name': handler_name
                }
                if bug_id in bug_objects:
                    bug_objects[bug_id]['files_data'].append(bug_file_data)
                else:
                    bug_objects[bug_id] = {
                        'bug_id': bug_id,
                        'files_data': [bug_file_data]
                    }

                if report:
                    if bug_file_path not in bug_files_path:
                        bug_files_path.append(bug_file_path)

                    file_bug_data = {
                        'bug_id': bug_id,
                        'line_number': line_number,
                        'handler_name': handler_name
                    }
                    if bug_file_path in files_data:
                        files_data[bug_file_path].append(file_bug_data)
                    else:
                        files_data[bug_file_path] = [file_bug_data]

        if report:
            raw_parse_time = round(time.time() - self.reporter.start_time, 2)
            self.reporter.output_status(
                'found {0} bugs usage in {1} files (occurrences {2})'
                ' in {3} seconds'.format(
                    len(bug_objects),
                    len(bug_files_path),
                    occurrences_counter,
                    raw_parse_time
                )
            )
        if bulk:
            if report:
                self.reporter.output_status('getting bugs info ...')

            for chunk_ids in chunks(list(bug_objects.keys()), chunk_size):
                chunk_data = self.bz_reader.get_bug_data_in_bulk(chunk_ids)
                for bug_id, bug_data in chunk_data.items():
                    bug_objects[bug_id]['bug_data'] = bug_data

        if report:
            self.reporter.output_status('generating report ...')
            self.reporter.write_header()
            for file_path in bug_files_path:
                for file_bug_data in files_data[file_path]:
                    bug_id = file_bug_data['bug_id']
                    data = bug_objects[bug_id]
                    self.reporter.write(
                        bug_id,
                        data.get('bug_data',
                                 self.bz_reader.get_bug_data(bug_id)),
                        file_bug_data['handler_name'],
                        file_path,
                        file_bug_data['line_number']
                    )
            self.reporter.stop()

        return bug_objects

    def get_bugs_status(self):
        self.parse(report=False)
        return self.bz_reader.bugs_status()
