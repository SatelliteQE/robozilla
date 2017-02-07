
BUGZILLA_ENVIRON_USER_NAME = 'BUGZILLA_USER_NAME'
BUGZILLA_ENVIRON_USER_PASSWORD_NAME = 'BUGZILLA_USER_PASSWORD'
BUGZILLA_URL = "https://bugzilla.redhat.com/xmlrpc.cgi"

FILE_NAME_PATTERN = '*.py'

DEFAULT_INCLUDE_FIELDS = [
    'id',
    'status',
    'whiteboard',
    'resolution',
    'flags',
    # getting dupe_of field makes request very slow
    # add this field explicitly and also follow_duplicates=True
    # 'dupe_of',
]
