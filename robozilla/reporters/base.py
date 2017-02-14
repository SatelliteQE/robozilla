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
    def start_time(self):
        return self._start_time

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

    def output_warn(self, *args):
        print(*args)

    def output_status(self, *args):
        print(*args)

    def output(self, *args):
        print(*args)

    def output_recursive(self, bug_data, field_name, title, init_tab=''):
        field_data = bug_data.get(field_name)
        ind = 4
        while field_data is not None:
            tab_str = ' ' * ind + init_tab
            self.output('{0} {1}:'.format(tab_str, title))
            self.output('{0} - {1} - {2} - {3}'.format(
                tab_str,
                self._left_just_string(str(field_data['id']), 10),
                self._left_just_string(field_data['status_resolution'],
                                       22),
                self._get_flags_string(field_data.get('flags', '')))
            )
            field_data = field_data.get(field_name)
            ind *= 2

    def output_list(self, bug_data, field_name, title, init_tab=''):
        field_list = bug_data.get(field_name, None)
        if field_list:
            if isinstance(field_list, dict):
                field_list = list(field_list.values())
            tab_str = ' ' * 4 + init_tab
            self.output('{0} {1}:'.format(tab_str, title))
            for field_entry in field_list:
                self.output('{0} - {1} - {2} - {3}'.format(
                    tab_str,
                    self._left_just_string(str(field_entry['id']), 10),
                    self._left_just_string(field_entry['status_resolution'],
                                           22),
                    self._get_flags_string(field_entry.get('flags', '')))
                )

    def write(self, bug_id, bug_data, handler_name, file_path,
              file_line_number):
        """Write the bug to something print for the moment"""
        if not bug_data:
            bug_data = {}
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

        self.output_recursive(bug_data, 'duplicate_of', 'DUPLICATE OF')
        self.output_list(bug_data, 'other_clones', 'OTHER CLONES')
        # todo a command line option to choose from the two representation
        # for a detailed report
        # self.output_list(bug_data, 'clones', 'CLONES')
        # self.output_recursive(bug_data, 'clone_of', 'CLONE OF')
        # # get all the clones of clone_of
        # bug_clone_of_data = bug_data.get('clone_of', None)
        # if bug_clone_of_data:
        #     self.output_list(bug_clone_of_data, 'clones', 'CLONES',
        #                      init_tab=' ' * 4)

        self.output_list(bug_data, 'dependent_on', 'DEPEND ON')

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
