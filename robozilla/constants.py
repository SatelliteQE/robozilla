
BUGZILLA_ENVIRON_USER_NAME = 'BUGZILLA_USER_NAME'
BUGZILLA_ENVIRON_USER_PASSWORD_NAME = 'BUGZILLA_USER_PASSWORD'
BUGZILLA_QUERY_PRODUCT = 'Red Hat Satellite 6'
BUGZILLA_URL = 'https://bugzilla.redhat.com/xmlrpc.cgi'

REDMINE_URL = 'http://projects.theforeman.org'

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

COVERAGE_REJECTED = "qe_test_coverage-"
COVERAGE_AUTOMATED = "qe_test_coverage+"
COVERAGE_BACKLOG = "qe_test_coverage?"
COVERAGE_INCLUDE_FIELDS = ['id']

# BUGZILLA QUERY
BUGZILLA_QUERY_URL = "https://bugzilla.redhat.com/query.cgi"
DEFAULT_QUERY_INCLUDE_FIELDS = ['id', 'summary', 'flags']


BZ_OPEN_STATUSES = [
    'NEW',
    'ASSIGNED',
    'POST',
    'MODIFIED'
]
BZ_CLOSED_STATUSES = [
    'ON_QA',
    'VERIFIED',
    'RELEASE_PENDING',
    'CLOSED'
]
