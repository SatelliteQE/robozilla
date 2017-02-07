

from tests.files.decorators import skip_if_bug_open, bz_bug_is_open


@skip_if_bug_open('bugzilla', 1405428)
class t_a(object):

    @skip_if_bug_open('bugzilla', 1219610)
    def func_1(self):
        """
        simple decorated function
        """

        if bz_bug_is_open(1328925):
            pass
