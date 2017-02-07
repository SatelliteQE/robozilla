
import functools


def skip_if_bug_open(bug_type, bug_id):
    """
    simple decorator to imitate the robottelo decorator
    """
    def main_wrapper(func):

        @functools.wraps(func)
        def function_wrapper(*args, **kw):
            return func(*args, **kw)

        return function_wrapper

    return main_wrapper


def bz_bug_is_open(bug_id):
    """simple decorator to imitate the robottelo function"""
    return False

