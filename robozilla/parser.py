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

    def __init__(self, files_provider, filters=None, reporter=None,
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

    def _parse_file(self, file_path):
        with open(file_path) as fr:
            line_number = 0
            for line in fr:
                for filter_handler in self.filters:
                    bug_ids = filter_handler.retrieve(line)
                    for bug_id in bug_ids:
                        yield (bug_id, file_path, line_number,
                               filter_handler.name)

                line_number += 1

    def parse(self, report=False, bulk=True, chunk_size=150):
        if report:
            self.reporter.start()

        bug_objects = {}
        for file_path in self.files_provider.get_files():
            for data in self._parse_file(file_path):
                bug_id, bug_file_path, line_number, handler_name = data
                bug_objects[bug_id] = {
                    'bug_id': bug_id,
                    'bug_file_path': bug_file_path,
                    'line_number': line_number,
                    'handler_name': handler_name
                }

        if bulk:
            for chunk_ids in chunks(list(bug_objects.keys()), chunk_size):
                chunk_data = self.bz_reader.get_bug_data_in_bulk(chunk_ids)
                for bug_id, bug_data in chunk_data.items():
                    bug_objects[bug_id]['bug_data'] = bug_data

        if report:
            self.reporter.output('{} bugs found'.format(len(bug_objects)))
            self.reporter.write_header()
            for bug_id, data in bug_objects.items():
                self.reporter.write(
                    bug_id,
                    data.get('bug_data', self.bz_reader.get_bug_data(bug_id)),
                    data['handler_name'],
                    data['bug_file_path'],
                    data['line_number']
                )
            self.reporter.stop()

        return bug_objects

    def get_bugs_status(self):
        self.parse(report=False)
        return self.bz_reader.bugs_status()
