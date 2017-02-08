
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
    # getting dupe_of, cf_clone_of and depends_on fields
    # makes request very slow
    # add this fields explicitly and also follow_duplicates=True
    # follow_clones=True
    # 'dupe_of',
    # 'cf_clone_of',
    # 'depends_on',
]

DUPLICATES_FIELD = 'dupe_of'
CLONES_FIELD = 'cf_clone_of'
DEPENDENT_FIELD = 'depends_on'
