import six

from robozilla.bz import BZReader
from robozilla.filters import BZDecorator, BZIsOpen
from robozilla.providers.fs import FilesProvider
from robozilla.reporters import RawReporter


class Parser(object):

    def __init__(self, files_provider, filters=None, reporter=None,
                 bz_reader=None, enviroment=None):

        if isinstance(files_provider, six.string_types):
                files_provider = FilesProvider(files_provider)

        self.files_provider = files_provider
        self.filters = filters if filters else [BZDecorator, BZIsOpen]
        self.bz_reader = bz_reader if bz_reader else BZReader()
        self.reporter = reporter if reporter else (
            RawReporter(bz_reader=bz_reader, environment=enviroment))

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

    def parse(self, report=True):
        self.reporter.start()
        for file_path in self.files_provider.get_files():
            for data in self._parse_file(file_path):
                bug_id, bug_file_path, line_number, handler_name = data
                bug_data = self.bz_reader.get_bug_data(bug_id)
                if report:
                    self.reporter.write(bug_id, bug_data, handler_name,
                                        bug_file_path, line_number)
        self.reporter.stop()

    def get_bugs_status(self):
        self.parse(report=False)
        return self.bz_reader.bugs_status()
