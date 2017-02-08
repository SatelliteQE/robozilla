Robottelo Bugzilla Parser
=========================

This is an early stage version

Install:
________

To install the latest release version::

    pip install robozilla


to install from github master branch::

    pip install https://github.com/ldjebran/robozilla/tarball/master


Basic usage:
____________

Go to robottelo folder to scan and launch the command::

    robozilla

or type::

    robozilla path_to_scan


type --help for more command line options::

    robozilla --help
    Usage: robozilla [OPTIONS] [SCAN_DIR]

    Options:
      --filters TEXT                  The filter to use when scanning,
                                      default=all, available: all, decorator,
                                      function
      --warn / --no-warn              Whether to output the warnings, default is
                                      warn
      --all / --no-all                this to get all duplicates clones depends
                                      bug info,  default is no-all
      --duplicates / --no-duplicates  Whether to get duplicates of bug info,
                                      default is no-duplicates
      --clones / --no-clones          Whether to get clones of bug info, default
                                      is no-clones
      --depends / --no-depends        Whether to get depends on bug info, default
                                      is no-depends
      --echo / --no-echo              Whether to echo entry parameters, default is
                                      echo
      --user TEXT                     The bugzilla user
      --password TEXT                 The bugzilla user password
      --help                          Show this message and exit.


    SCAN_DIR the directory path to scan, if omitted the default is the current directory


Milestones:

    milestone 1:
      * parser optimization
      * works related to doc, installer, unittests and TravisCI
      * find bugzilla ids work around usage in robottelo code and analyze their states
      * make recommendation and warn about critical or possible problems
      * should be able to be used as a standalone parser or as a library

    milestone 2:
      * integration with automation
      * integrate with jenkins via API to be able to read test PASS/SKIP/FAIL and compare to bug ids in code
      * warn about possible bugs fixture regression or bugs work around failure


a very early stage sample output:

.. code-block:: sh

    user:~/projects/robottelo-fork$ robozilla --all
    scanning: /home/user/projects/robottelo-fork
    warn: True
    duplicates: True
    clones: True
    depends: True
    filters: all
    connecting to bugzilla without credentials
    WARNING: bz_bug_is_open handler string found, but no bug id retrieved
       line : 248 file: ../robottelo-fork/tests/foreman/cli/test_discoveryrule.py
       line content: if bug_id is not None and bz_bug_is_open(bug_id):
    WARNING: bz_bug_is_open handler string found, but no bug id retrieved
       line : 64 file: ../robottelo-fork/tests/foreman/ui/test_bookmark.py
       line content: if skip and (skip is True or bz_bug_is_open(skip)):
    WARNING: bz_bug_is_open handler string found, but no bug id retrieved
       line : 132 file: ../robottelo-fork/tests/foreman/ui/test_domain.py
       line content: if bug_id is not None and bz_bug_is_open(bug_id):
    found 109 bugs usage in 71 files (occurrences 221) in 0.19 seconds
    getting bugs info ...
    generating report ...
    Handler           | BZ         | State                  | Flags                  | Line -> File
    skip_if_bug_open  | 1156555    | CLOSED_WONTFIX         | sat-backlog+           | 126 -> ../robottelo-fork/tests/foreman/api/test_activationkey.py
    skip_if_bug_open  | 1401519    | NEW                    | sat-6.3.0?             | 58 -> ../robottelo-fork/tests/foreman/api/test_architecture.py
    skip_if_bug_open  | 1302725    | VERIFIED               | sat-6.3.0+             | 199 -> ../robottelo-fork/tests/foreman/api/test_bookmarks.py
    skip_if_bug_open  | 1374253    | VERIFIED               | sat-6.3.0+             | 1458 -> ../robottelo-fork/tests/foreman/api/test_classparameters.py
    skip_if_bug_open  | 1147100    | ASSIGNED               | sat-backlog+           | 1034 -> ../robottelo-fork/tests/foreman/api/test_contentview.py
    skip_if_bug_open  | 1242534    | CLOSED_ERRATA          | sat-6.2.0+             | 647 -> ../robottelo-fork/tests/foreman/api/test_contentviewfilter.py
    skip_if_bug_open  | 1349364    | VERIFIED               | sat-6.3.0+, sat-6.2.z+ | 129 -> ../robottelo-fork/tests/foreman/api/test_discoveredhost.py
    bz_bug_is_open    | 1392919    | NEW                    | sat-backlog?           | 148 -> ../robottelo-fork/tests/foreman/api/test_discoveredhost.py
    skip_if_bug_open  | 1217635    | CLOSED_WONTFIX         | sat-backlog?           | 608 -> ../robottelo-fork/tests/foreman/api/test_docker.py
    skip_if_bug_open  | 1282431    | CLOSED_ERRATA          | sat-6.1.z+             | 1231 -> ../robottelo-fork/tests/foreman/api/test_docker.py
    bz_bug_is_open    | 1374669    | CLOSED_DUPLICATE       | sat-backlog?           | 98 -> ../robottelo-fork/tests/foreman/api/test_errata.py
         DUPLICATE OF:
         - 1108106    - CLOSED_ERRATA          - sat-6.2.0+
    bz_bug_is_open    | 1203865    | POST                   | sat-6.3.0+             | 129 -> ../robottelo-fork/tests/foreman/api/test_host.py
    bz_bug_is_open    | 1210001    | NEW                    | sat-backlog?           | 146 -> ../robottelo-fork/tests/foreman/api/test_host.py
    skip_if_bug_open  | 1325989    | CLOSED_ERRATA          | sat-6.2.z+             | 141 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1325989    | CLOSED_ERRATA          | sat-6.2.z+             | 157 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1325989    | CLOSED_ERRATA          | sat-6.2.z+             | 173 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1325989    | CLOSED_ERRATA          | sat-6.2.z+             | 191 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1325989    | CLOSED_ERRATA          | sat-6.2.z+             | 209 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1222118    | CLOSED_ERRATA          | sat-6.1.z+             | 46 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 583 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 602 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 630 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 658 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 690 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 711 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 750 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 781 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 801 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 829 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 893 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 913 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 934 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 964 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 987 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 1007 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 1027 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1378009    | ASSIGNED               | sat-6.3.0+             | 1053 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    bz_bug_is_open    | 1118015    | NEW                    | sat-backlog+           | 231 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    skip_if_bug_open  | 1122257    | CLOSED_ERRATA          | sat-6.2.0+             | 242 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    bz_bug_is_open    | 1378009    | ASSIGNED               | sat-6.3.0+             | 305 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    bz_bug_is_open    | 1378009    | ASSIGNED               | sat-6.3.0+             | 392 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
         DEPEND ON:
         - 1374253    - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1230902    | CLOSED_WONTFIX         | sat-backlog+           | 122 -> ../robottelo-fork/tests/foreman/api/test_operatingsystem.py
    skip_if_bug_open  | 1328935    | VERIFIED               | sat-6.3.0+             | 308 -> ../robottelo-fork/tests/foreman/api/test_operatingsystem.py
    skip_if_bug_open  | 1230865    | NEW                    | sat-backlog+           | 288 -> ../robottelo-fork/tests/foreman/api/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 321 -> ../robottelo-fork/tests/foreman/api/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 342 -> ../robottelo-fork/tests/foreman/api/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 373 -> ../robottelo-fork/tests/foreman/api/test_organization.py
    skip_if_bug_open  | 1103157    | CLOSED_WONTFIX         | sat-backlog+           | 415 -> ../robottelo-fork/tests/foreman/api/test_organization.py
    skip_if_bug_open  | 1229384    | CLOSED_ERRATA          | sat-6.2.0+             | 37 -> ../robottelo-fork/tests/foreman/api/test_partitiontable.py
    skip_if_bug_open  | 1310422    | NEW                    | sat-backlog?           | 232 -> ../robottelo-fork/tests/foreman/api/test_product.py
    skip_if_bug_open  | 1378442    | NEW                    | sat-backlog?           | 683 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    skip_if_bug_open  | 1311113    | NEW                    | sat-backlog?           | 741 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 817 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 846 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 874 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    skip_if_bug_open  | 1194476    | NEW                    | sat-backlog+           | 1103 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    bz_bug_is_open    | 1112657    | CLOSED_ERRATA          | sat-6.1.0+             | 42 -> ../robottelo-fork/tests/foreman/api/test_role.py
    bz_bug_is_open    | 1112657    | CLOSED_ERRATA          | sat-6.1.0+             | 57 -> ../robottelo-fork/tests/foreman/api/test_role.py
    bz_bug_is_open    | 1112657    | CLOSED_ERRATA          | sat-6.1.0+             | 76 -> ../robottelo-fork/tests/foreman/api/test_role.py
    skip_if_bug_open  | 1398695    | POST                   | sat-6.3.0?             | 78 -> ../robottelo-fork/tests/foreman/api/test_smartproxy.py
    skip_if_bug_open  | 1199150    | NEW                    | sat-backlog?           | 458 -> ../robottelo-fork/tests/foreman/api/test_syncplan.py
    skip_if_bug_open  | 1199150    | NEW                    | sat-backlog?           | 511 -> ../robottelo-fork/tests/foreman/api/test_syncplan.py
    skip_if_bug_open  | 1202564    | CLOSED_CURRENTRELEASE  | sat-6.1.0+             | 36 -> ../robottelo-fork/tests/foreman/api/test_template.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 54 -> ../robottelo-fork/tests/foreman/api/test_template.py
    skip_if_bug_open  | 1369737    | VERIFIED               | sat-6.3.0+, sat-6.2.z+ | 73 -> ../robottelo-fork/tests/foreman/api/test_template_combination.py
    skip_if_bug_open  | 1369737    | VERIFIED               | sat-6.3.0+, sat-6.2.z+ | 90 -> ../robottelo-fork/tests/foreman/api/test_template_combination.py
    skip_if_bug_open  | 1375857    | CLOSED_WORKSFORME      | sat-backlog?           | 236 -> ../robottelo-fork/tests/foreman/api/test_variables.py
    skip_if_bug_open  | 1375643    | NEW                    | sat-backlog?           | 766 -> ../robottelo-fork/tests/foreman/api/test_variables.py
         DEPEND ON:
         - 1411069    - ASSIGNED               - sat-6.3.0?
    skip_if_bug_open  | 1110476    | NEW                    | sat-backlog?           | 608 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1360239    | ON_QA                  | sat-6.3.0+, sat-6.2.z+ | 668 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1360239    | ON_QA                  | sat-6.3.0+, sat-6.2.z+ | 692 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1339211    | CLOSED_ERRATA          | sat-6.2.0+             | 751 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1336716    | CLOSED_ERRATA          | sat-6.2.z+             | 916 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1336716    | CLOSED_ERRATA          | sat-6.2.z+             | 956 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1360239    | ON_QA                  | sat-6.3.0+, sat-6.2.z+ | 1218 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1398695    | POST                   | sat-6.3.0?             | 83 -> ../robottelo-fork/tests/foreman/cli/test_capsule.py
    skip_if_bug_open  | 1214312    | CLOSED_WONTFIX         | sat-backlog+           | 253 -> ../robottelo-fork/tests/foreman/cli/test_computeresource.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 236 -> ../robottelo-fork/tests/foreman/cli/test_contentview.py
    skip_if_bug_open  | 1317057    | CLOSED_ERRATA          | sat-6.2.0+             | 329 -> ../robottelo-fork/tests/foreman/cli/test_contentview.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 866 -> ../robottelo-fork/tests/foreman/cli/test_contentview.py
    skip_if_bug_open  | 1343006    | CLOSED_ERRATA          | sat-6.2.0+             | 946 -> ../robottelo-fork/tests/foreman/cli/test_contentview.py
         DEPEND ON:
         - 1353471    - CLOSED_ERRATA          - sat-6.2.0+
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 1979 -> ../robottelo-fork/tests/foreman/cli/test_contentview.py
    skip_if_bug_open  | 1236532    | CLOSED_ERRATA          | sat-6.2.0+             | 140 -> ../robottelo-fork/tests/foreman/cli/test_contentviewfilter.py
    skip_if_bug_open  | 1356906    | VERIFIED               | sat-6.3.0+             | 166 -> ../robottelo-fork/tests/foreman/cli/test_contentviewfilter.py
    skip_if_bug_open  | 1343006    | CLOSED_ERRATA          | sat-6.2.0+             | 265 -> ../robottelo-fork/tests/foreman/cli/test_contentviewfilter.py
         DEPEND ON:
         - 1353471    - CLOSED_ERRATA          - sat-6.2.0+
    bz_bug_is_open    | 1328943    | CLOSED_ERRATA          | sat-6.2.0+             | 650 -> ../robottelo-fork/tests/foreman/cli/test_contentviewfilter.py
    skip_if_bug_open  | 1388642    | POST                   | sat-6.3.0+             | 834 -> ../robottelo-fork/tests/foreman/cli/test_contentviewfilter.py
    skip_if_bug_open  | 1377990    | POST                   | sat-6.3.0?             | 148 -> ../robottelo-fork/tests/foreman/cli/test_discoveryrule.py
    skip_if_bug_open  | 1377990    | POST                   | sat-6.3.0?             | 310 -> ../robottelo-fork/tests/foreman/cli/test_discoveryrule.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 476 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 511 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 584 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 658 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 776 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 835 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 1007 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 1063 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1282431    | CLOSED_ERRATA          | sat-6.1.z+             | 1496 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1230915    | CLOSED_ERRATA          | sat-6.1.z+             | 1547 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1269196    | CLOSED_WONTFIX         | sat-backlog+           | 1548 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1230915    | CLOSED_ERRATA          | sat-6.1.z+             | 1581 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1269208    | NEW                    | sat-backlog?           | 1582 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1230915    | CLOSED_ERRATA          | sat-6.1.z+             | 1641 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    bz_bug_is_open    | 1398392    | POST                   | sat-6.3.0?, sat-6.2.z? | 50 -> ../robottelo-fork/tests/foreman/cli/test_domain.py
    bz_bug_is_open    | 1398392    | POST                   | sat-6.3.0?, sat-6.2.z? | 77 -> ../robottelo-fork/tests/foreman/cli/test_domain.py
    bz_bug_is_open    | 1403947    | NEW                    | sat-6.3.0?             | 1578 -> ../robottelo-fork/tests/foreman/cli/test_errata.py
    skip_if_bug_open  | 1401469    | POST                   | sat-6.3.0?             | 66 -> ../robottelo-fork/tests/foreman/cli/test_filter.py
    skip_if_bug_open  | 1401469    | POST                   | sat-6.3.0?             | 85 -> ../robottelo-fork/tests/foreman/cli/test_filter.py
    skip_if_bug_open  | 1401469    | POST                   | sat-6.3.0?             | 189 -> ../robottelo-fork/tests/foreman/cli/test_filter.py
    bz_bug_is_open    | 1219610    | CLOSED_WONTFIX         | sat-backlog+           | 98 -> ../robottelo-fork/tests/foreman/cli/test_hammer.py
    bz_bug_is_open    | 1219610    | CLOSED_WONTFIX         | sat-backlog+           | 116 -> ../robottelo-fork/tests/foreman/cli/test_hammer.py
    skip_if_bug_open  | 1343392    | VERIFIED               | sat-6.3.0+             | 722 -> ../robottelo-fork/tests/foreman/cli/test_host.py
    skip_if_bug_open  | 1343392    | VERIFIED               | sat-6.3.0+             | 745 -> ../robottelo-fork/tests/foreman/cli/test_host.py
    skip_if_bug_open  | 1328925    | CLOSED_ERRATA          | sat-6.2.0+             | 190 -> ../robottelo-fork/tests/foreman/cli/test_host_collection.py
    skip_if_bug_open  | 1328925    | CLOSED_ERRATA          | sat-6.2.0+             | 212 -> ../robottelo-fork/tests/foreman/cli/test_host_collection.py
    skip_if_bug_open  | 1245334    | CLOSED_WONTFIX         | sat-backlog+           | 233 -> ../robottelo-fork/tests/foreman/cli/test_host_collection.py
    skip_if_bug_open  | 1328925    | CLOSED_ERRATA          | sat-6.2.0+             | 257 -> ../robottelo-fork/tests/foreman/cli/test_host_collection.py
    skip_if_bug_open  | 1354544    | CLOSED_CURRENTRELEASE  | sat-backlog?           | 189 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
    skip_if_bug_open  | 1313056    | NEW                    | sat-backlog?           | 218 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
    bz_bug_is_open    | 1395254    | POST                   | sat-6.3.0?             | 335 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
    bz_bug_is_open    | 1313056    | NEW                    | sat-backlog?           | 360 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
    skip_if_bug_open  | 1354568    | POST                   | sat-backlog?           | 366 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
         DEPEND ON:
         - 1398392    - POST                   - sat-6.3.0?, sat-6.2.z?
    skip_if_bug_open  | 1354568    | POST                   | sat-backlog?           | 389 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
         DEPEND ON:
         - 1398392    - POST                   - sat-6.3.0?, sat-6.2.z?
    skip_if_bug_open  | 1354568    | POST                   | sat-backlog?           | 412 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
         DEPEND ON:
         - 1398392    - POST                   - sat-6.3.0?, sat-6.2.z?
    bz_bug_is_open    | 1263650    | CLOSED_WONTFIX         | sat-backlog?           | 127 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    bz_bug_is_open    | 1260722    | NEW                    | sat-backlog+           | 285 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    bz_bug_is_open    | 1263650    | CLOSED_WONTFIX         | sat-backlog?           | 1212 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1325880    | CLOSED_ERRATA          | sat-6.2.0+             | 1310 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    bz_bug_is_open    | 1226981    | CLOSED_ERRATA          | sat-6.1.z+             | 1379 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1238247    | NEW                    | sat-backlog?           | 1524 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1238247    | NEW                    | sat-backlog?           | 1554 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1238247    | NEW                    | sat-backlog?           | 1594 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1267224    | CLOSED_WONTFIX         | sat-backlog+           | 1595 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1325880    | CLOSED_ERRATA          | sat-6.2.0+             | 1665 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1325880    | CLOSED_ERRATA          | sat-6.2.0+             | 1705 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1325124    | CLOSED_ERRATA          | sat-6.2.0+             | 1761 -> ../robottelo-fork/tests/foreman/cli/test_import.py
         DEPEND ON:
         - 1337746    - CLOSED_ERRATA          - sat-6.2.0+
    skip_if_bug_open  | 1233612    | VERIFIED               | sat-6.3.0+             | 79 -> ../robottelo-fork/tests/foreman/cli/test_location.py
    skip_if_bug_open  | 1234287    | POST                   | sat-6.2.z+             | 314 -> ../robottelo-fork/tests/foreman/cli/test_location.py
    skip_if_bug_open  | 1395110    | CLOSED_DUPLICATE       | sat-6.3.0?             | 605 -> ../robottelo-fork/tests/foreman/cli/test_location.py
         DUPLICATE OF:
         - 1398695    - POST                   - sat-6.3.0?
    skip_if_bug_open  | 1395110    | CLOSED_DUPLICATE       | sat-6.3.0?             | 631 -> ../robottelo-fork/tests/foreman/cli/test_location.py
         DUPLICATE OF:
         - 1398695    - POST                   - sat-6.3.0?
    skip_if_bug_open  | 1395110    | CLOSED_DUPLICATE       | sat-6.3.0?             | 656 -> ../robottelo-fork/tests/foreman/cli/test_location.py
         DUPLICATE OF:
         - 1398695    - POST                   - sat-6.3.0?
    skip_if_bug_open  | 1395110    | CLOSED_DUPLICATE       | sat-6.3.0?             | 685 -> ../robottelo-fork/tests/foreman/cli/test_location.py
         DUPLICATE OF:
         - 1398695    - POST                   - sat-6.3.0?
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 247 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 275 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 340 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 364 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 430 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 456 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 522 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 547 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 634 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 665 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 735 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 760 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 973 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 1001 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 1227 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 1255 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 1334 -> ../robottelo-fork/tests/foreman/cli/test_organization.py
    skip_if_bug_open  | 1229384    | CLOSED_ERRATA          | sat-6.2.0+             | 29 -> ../robottelo-fork/tests/foreman/cli/test_partitiontable.py
    bz_bug_is_open    | 1219490    | CLOSED_WONTFIX         | sat-backlog+           | 319 -> ../robottelo-fork/tests/foreman/cli/test_product.py
    skip_if_bug_open  | 1283173    | CLOSED_ERRATA          | sat-6.2.0+             | 45 -> ../robottelo-fork/tests/foreman/cli/test_puppetmodule.py
    skip_if_bug_open  | 1103944    | CLOSED_WORKSFORME      | sat-6.2.0+             | 412 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
         DEPEND ON:
         - 1103945    - CLOSED_CURRENTRELEASE  - sat-6.0.4+
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 687 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 718 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 751 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    bz_bug_is_open    | 1413145    | NEW                    | sat-6.3.0?             | 1081 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1343006    | CLOSED_ERRATA          | sat-6.2.0+             | 1142 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
         DEPEND ON:
         - 1353471    - CLOSED_ERRATA          - sat-6.2.0+
    skip_if_bug_open  | 1378442    | NEW                    | sat-backlog?           | 1165 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1370108    | NEW                    | sat-backlog?           | 1230 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1226425    | CLOSED_WONTFIX         | sat-backlog+           | 163 -> ../robottelo-fork/tests/foreman/cli/test_subscription.py
    skip_if_bug_open  | 1336790    | CLOSED_ERRATA          | sat-6.2.0+             | 278 -> ../robottelo-fork/tests/foreman/cli/test_syncplan.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 133 -> ../robottelo-fork/tests/foreman/cli/test_template.py
    skip_if_bug_open  | 1204686    | CLOSED_WONTFIX         | sat-backlog?           | 308 -> ../robottelo-fork/tests/foreman/cli/test_user.py
    skip_if_bug_open  | 1204667    | POST                   | sat-6.4.0+             | 543 -> ../robottelo-fork/tests/foreman/cli/test_user.py
    skip_if_bug_open  | 1138553    | CLOSED_ERRATA          | sat-6.2.0+             | 908 -> ../robottelo-fork/tests/foreman/cli/test_user.py
    skip_if_bug_open  | 1138553    | CLOSED_ERRATA          | sat-6.2.0+             | 959 -> ../robottelo-fork/tests/foreman/cli/test_user.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 468 -> ../robottelo-fork/tests/foreman/cli/test_usergroup.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 490 -> ../robottelo-fork/tests/foreman/cli/test_usergroup.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 512 -> ../robottelo-fork/tests/foreman/cli/test_usergroup.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 534 -> ../robottelo-fork/tests/foreman/cli/test_usergroup.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 556 -> ../robottelo-fork/tests/foreman/cli/test_usergroup.py
    skip_if_bug_open  | 1395229    | POST                   | sat-6.3.0+             | 578 -> ../robottelo-fork/tests/foreman/cli/test_usergroup.py
    skip_if_bug_open  | 1367032    | VERIFIED               | sat-6.3.0+, sat-6.2.z+ | 318 -> ../robottelo-fork/tests/foreman/cli/test_variables.py
    skip_if_bug_open  | 1371794    | POST                   | sat-6.3.0+             | 1332 -> ../robottelo-fork/tests/foreman/cli/test_variables.py
    bz_bug_is_open    | 1166875    | NEW                    | sat-backlog?           | 821 -> ../robottelo-fork/tests/foreman/endtoend/test_api_endtoend.py
    bz_bug_is_open    | 1325995    | VERIFIED               | sat-6.3.0+             | 926 -> ../robottelo-fork/tests/foreman/endtoend/test_api_endtoend.py
    bz_bug_is_open    | 1328202    | CLOSED_ERRATA          | sat-6.2.0+             | 356 -> ../robottelo-fork/tests/foreman/endtoend/test_cli_endtoend.py
    bz_bug_is_open    | 1326101    | NEW                    | sat-backlog?           | 420 -> ../robottelo-fork/tests/foreman/endtoend/test_cli_endtoend.py
    bz_bug_is_open    | 1191422    | CLOSED_ERRATA          | sat-6.1.0+             | 401 -> ../robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py
    bz_bug_is_open    | 1191422    | CLOSED_ERRATA          | sat-6.1.0+             | 410 -> ../robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py
    bz_bug_is_open    | 1191422    | CLOSED_ERRATA          | sat-6.1.0+             | 417 -> ../robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py
    bz_bug_is_open    | 1191541    | CLOSED_CURRENTRELEASE  | sat-6.1.0+             | 434 -> ../robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py
    bz_bug_is_open    | 1246152    | CLOSED_ERRATA          | sat-6.2.0+             | 100 -> ../robottelo-fork/tests/foreman/installer/test_installer.py
    skip_if_bug_open  | 1390355    | CLOSED_DUPLICATE       | sat-6.3.0?             | 140 -> ../robottelo-fork/tests/foreman/sys/test_hot_backup.py
         DUPLICATE OF:
         - 1384901    - ON_QA                  - sat-6.3.0+, sat-6.2.z+
    skip_if_bug_open  | 1221971    | ASSIGNED               | sat-6.3.0+             | 351 -> ../robottelo-fork/tests/foreman/ui/test_adusergroup.py
    skip_if_bug_open  | 1326633    | NEW                    | sat-backlog+           | 226 -> ../robottelo-fork/tests/foreman/ui/test_bookmark.py
    skip_if_bug_open  | 1324484    | CLOSED_ERRATA          | sat-6.2.0+             | 453 -> ../robottelo-fork/tests/foreman/ui/test_bookmark.py
    skip_if_bug_open  | 1324484    | CLOSED_ERRATA          | sat-6.2.0+             | 493 -> ../robottelo-fork/tests/foreman/ui/test_bookmark.py
    skip_if_bug_open  | 1295179    | CLOSED_ERRATA          | sat-6.2.0+             | 1166 -> ../robottelo-fork/tests/foreman/ui/test_classparameters.py
    skip_if_bug_open  | 1378486    | POST                   | sat-6.3.0+             | 231 -> ../robottelo-fork/tests/foreman/ui/test_discoveryrule.py
    skip_if_bug_open  | 1308831    | VERIFIED               | sat-6.3.0+             | 299 -> ../robottelo-fork/tests/foreman/ui/test_discoveryrule.py
    skip_if_bug_open  | 1378486    | POST                   | sat-6.3.0+             | 542 -> ../robottelo-fork/tests/foreman/ui/test_discoveryrule.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1437 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1461 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1490 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1518 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1547 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1576 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1383729    | POST                   | sat-6.3.0+             | 413 -> ../robottelo-fork/tests/foreman/ui/test_errata.py
    skip_if_bug_open  | 1210180    | CLOSED_WONTFIX         | sat-backlog+           | 726 -> ../robottelo-fork/tests/foreman/ui/test_gpgkey.py
    skip_if_bug_open  | 1210180    | CLOSED_WONTFIX         | sat-backlog+           | 1012 -> ../robottelo-fork/tests/foreman/ui/test_gpgkey.py
    skip_if_bug_open  | 1210180    | CLOSED_WONTFIX         | sat-backlog+           | 1323 -> ../robottelo-fork/tests/foreman/ui/test_gpgkey.py
    skip_if_bug_open  | 1414134    | NEW                    | sat-6.3.0?             | 729 -> ../robottelo-fork/tests/foreman/ui/test_host.py
    skip_if_bug_open  | 1300350    | NEW                    | sat-backlog?           | 137 -> ../robottelo-fork/tests/foreman/ui/test_hostcollection.py
    skip_if_bug_open  | 1418695    | CLOSED_DUPLICATE       | sat-6.3.0?             | 75 -> ../robottelo-fork/tests/foreman/ui/test_navigation.py
         DUPLICATE OF:
         - 1351464    - POST                   - sat-6.3.0+, sat-6.2.z+
    skip_if_bug_open  | 1079482    | CLOSED_WONTFIX         | sat-backlog+           | 156 -> ../robottelo-fork/tests/foreman/ui/test_organization.py
    skip_if_bug_open  | 1289571    | ON_QA                  | sat-6.3.0+             | 80 -> ../robottelo-fork/tests/foreman/ui/test_oscapcontent.py
    skip_if_bug_open  | 1293296    | ON_QA                  | sat-6.3.0+             | 116 -> ../robottelo-fork/tests/foreman/ui/test_oscappolicy.py
    skip_if_bug_open  | 1394390    | POST                   | sat-6.3.0+             | 139 -> ../robottelo-fork/tests/foreman/ui/test_packages.py
         CLONE OF:
         - 1386670    - CLOSED_ERRATA          - sat-6.2.z+
         DEPEND ON:
         - 1386670    - CLOSED_ERRATA          - sat-6.2.z+
    skip_if_bug_open  | 1394390    | POST                   | sat-6.3.0+             | 1454 -> ../robottelo-fork/tests/foreman/ui/test_repository.py
         CLONE OF:
         - 1386670    - CLOSED_ERRATA          - sat-6.2.z+
         DEPEND ON:
         - 1386670    - CLOSED_ERRATA          - sat-6.2.z+
    parse time:356.0 seconds





