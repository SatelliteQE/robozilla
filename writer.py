from __future__ import print_function


class BugReportWriter(object):

    def __init__(self):
        pass

    def write(self, bug_id, bug_data, handler_name, file_path,
              file_line_number):
        """Write the bug to something print for the moment"""
        if bug_data:
            bug_state = bug_data['state']
            bug_resolution = bug_data['resolution']
            bug_state_text = '{0}'.format(bug_state)
            if bug_resolution:
                bug_state_text = '{0}_{1}'.format(bug_state, bug_resolution)
        else:
            bug_state_text = 'NONE'

        print("found bz usage:", handler_name, bug_id, bug_state_text,
              file_path, 'line:', file_line_number)

    def finish_writing(self):
        raise NotImplementedError
