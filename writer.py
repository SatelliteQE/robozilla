from __future__ import print_function

import time


class BugReportWriter(object):

    def __init__(self):
        self._start_time = 0

    def start(self):
        self._start_time = time.time()

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

        print("found bz usage:", handler_name, bug_id, bug_state_text,
              file_path, 'line:', file_line_number)

    def finish(self):
        print('parse time:{0} seconds'.format(
            round((time.time() - self._start_time), 0)))
