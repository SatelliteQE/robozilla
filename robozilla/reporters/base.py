from __future__ import print_function

import time


class RawReporter(object):

    def __init__(self, bz_reader=None, environment=None):
        self._started = False
        self._start_time = 0
        self._end_time = 0
        self._environment = environment
        self.bz_reader = bz_reader

    def set_bz_reader(self, bz_reader):
        self.bz_reader = bz_reader

    def start(self):
        self._started = True
        self._start_time = time.time()
        self._end_time = 0

    @property
    def started(self):
        return self._started

    @property
    def finished(self):
        if not self.started and self._end_time:
            return True
        return False

    @property
    def parse_time(self):
        if self.finished:
            parse_time = self._end_time - self._start_time
        elif self.started:
            parse_time = time.time() - self._start_time
        else:
            parse_time = 0

        return parse_time

    @staticmethod
    def _left_just_string(text, number):
        return text.ljust(number)

    @staticmethod
    def _get_flags_string(flags):
        if not flags:
            flags = {}
        return ', '.join(
            ['{0}{1}'.format(key, value) for key, value in flags.items()]
        )

    def output(self, *args):
        print(*args)

    def write(self, bug_id, bug_data, handler_name, file_path,
              file_line_number):
        """Write the bug to something print for the moment"""
        if bug_data:
            bug_status = bug_data['status']
            bug_resolution = bug_data['resolution']
            bug_state_text = '{0}'.format(bug_status)
            if bug_resolution:
                bug_state_text = '{0}_{1}'.format(bug_status, bug_resolution)
        else:
            bug_state_text = 'NONE'

        self.output('{0} | {1} | {2} | {3} | {4} -> {5}'.format(
            self._left_just_string(handler_name, 17),
            self._left_just_string(str(bug_id), 10),
            self._left_just_string(bug_state_text, 22),
            self._left_just_string(
                self._get_flags_string(bug_data.get('flags', '')), 22),
            str(file_line_number),
            file_path
        ))

        duplicate_of_data = bug_data.get('duplicate_of')
        ind = 4
        while duplicate_of_data is not None:
            tab_str = ' '*ind
            self.output('{0} DUPLICATE OF:'.format(tab_str))
            self.output('{0} - {1} - {2} - {3}'.format(
                tab_str,
                self._left_just_string(str(duplicate_of_data['id']), 10),
                self._left_just_string(duplicate_of_data['status_resolution'],
                                       22),
                self._get_flags_string(duplicate_of_data.get('flags', '')))
            )
            duplicate_of_data = duplicate_of_data['duplicate_of']
            ind *= 2

    def write_header(self):
        self.output('{0} | {1} | {2} | {3} | {4} -> {5}'.format(
            self._left_just_string('Handler', 17),
            self._left_just_string('BZ', 10),
            self._left_just_string('State', 22),
            self._left_just_string('Flags', 22),
            'Line',
            'File'
        ))

    def stop(self, success=True):
        self._started = False
        self._end_time = time.time()
        print('parse time:{0} seconds'.format(round(self.parse_time, 0)))
