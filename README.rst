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

    user:~/projects/robottelo-fork$ robozilla
    /home/user/projects/robottelo-fork
    bz_bug_is_open    | 1252101    | CLOSED_WONTFIX         | sat-backlog?           | 35 -> ../robottelo-fork/robottelo/api/utils.py
    bz_bug_is_open    | 1328202    | CLOSED_ERRATA          | sat-6.2.0+             | 47 -> ../robottelo-fork/robottelo/cli/contenthost.py
    bz_bug_is_open    | 1332650    | NEW                    | sat-backlog+           | 585 -> ../robottelo-fork/robottelo/cli/factory.py
    bz_bug_is_open    | 1339696    | NEW                    | sat-backlog+           | 37 -> ../robottelo-fork/robottelo/cli/subscription.py
    bz_bug_is_open    | 1322012    | POST                   | sat-6.4.0+             | 40 -> ../robottelo-fork/robottelo/ui/bookmark.py
    bz_bug_is_open    | 1400535    | NEW                    | sat-backlog?           | 700 -> ../robottelo-fork/robottelo/ui/contentviews.py
    bz_bug_is_open    | 1233135    | NEW                    | sat-backlog+           | 55 -> ../robottelo-fork/robottelo/ui/discoveryrules.py
    bz_bug_is_open    | 1328627    | CLOSED_ERRATA          | sat-6.2.0+             | 25 -> ../robottelo-fork/robottelo/ui/navigator.py
    bz_bug_is_open    | 1339696    | NEW                    | sat-backlog+           | 40 -> ../robottelo-fork/robottelo/ui/subscription.py
    bz_bug_is_open    | 1339696    | NEW                    | sat-backlog+           | 48 -> ../robottelo-fork/robottelo/ui/subscription.py
    skip_if_bug_open  | 1156555    | CLOSED_WONTFIX         | sat-backlog+           | 126 -> ../robottelo-fork/tests/foreman/api/test_activationkey.py
    skip_if_bug_open  | 1302725    | VERIFIED               | sat-6.3.0+             | 199 -> ../robottelo-fork/tests/foreman/api/test_bookmarks.py
    bz_bug_is_open    | 1223494    | CLOSED_ERRATA          | sat-6.2.0+             | 99 -> ../robottelo-fork/tests/foreman/api/test_contentview.py
    skip_if_bug_open  | 1297308    | CLOSED_ERRATA          | sat-6.1.z+             | 176 -> ../robottelo-fork/tests/foreman/api/test_contentview.py
    skip_if_bug_open  | 1147100    | ASSIGNED               | sat-backlog+           | 991 -> ../robottelo-fork/tests/foreman/api/test_contentview.py
    skip_if_bug_open  | 1242534    | CLOSED_ERRATA          | sat-6.2.0+             | 647 -> ../robottelo-fork/tests/foreman/api/test_contentviewfilter.py
    skip_if_bug_open  | 1349364    | VERIFIED               | sat-6.3.0+, sat-6.2.z+ | 129 -> ../robottelo-fork/tests/foreman/api/test_discoveredhost.py
    bz_bug_is_open    | 1392919    | NEW                    | sat-backlog?           | 148 -> ../robottelo-fork/tests/foreman/api/test_discoveredhost.py
    skip_if_bug_open  | 1217635    | CLOSED_WONTFIX         | sat-backlog?           | 610 -> ../robottelo-fork/tests/foreman/api/test_docker.py
    skip_if_bug_open  | 1282431    | CLOSED_ERRATA          | sat-6.1.z+             | 1233 -> ../robottelo-fork/tests/foreman/api/test_docker.py
    bz_bug_is_open    | 1366573    | NEW                    | sat-backlog?           | 1377 -> ../robottelo-fork/tests/foreman/api/test_docker.py
    bz_bug_is_open    | 1414797    | MODIFIED               | sat-6.2.z+             | 1377 -> ../robottelo-fork/tests/foreman/api/test_docker.py
    bz_bug_is_open    | 1203865    | POST                   | sat-6.3.0+             | 124 -> ../robottelo-fork/tests/foreman/api/test_host.py
    bz_bug_is_open    | 1210001    | NEW                    | sat-backlog?           | 141 -> ../robottelo-fork/tests/foreman/api/test_host.py
    skip_if_bug_open  | 1415679    | POST                   | sat-6.2.z+             | 55 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1325989    | CLOSED_ERRATA          | sat-6.2.z+             | 142 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1325989    | CLOSED_ERRATA          | sat-6.2.z+             | 158 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1325989    | CLOSED_ERRATA          | sat-6.2.z+             | 174 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1325989    | CLOSED_ERRATA          | sat-6.2.z+             | 192 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1325989    | CLOSED_ERRATA          | sat-6.2.z+             | 210 -> ../robottelo-fork/tests/foreman/api/test_hostcollection.py
    skip_if_bug_open  | 1222118    | CLOSED_ERRATA          | sat-6.1.z+             | 46 -> ../robottelo-fork/tests/foreman/api/test_hostgroup.py
    bz_bug_is_open    | 1118015    | NEW                    | sat-backlog+           | 233 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    skip_if_bug_open  | 1122257    | CLOSED_ERRATA          | sat-6.2.0+             | 244 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    bz_bug_is_open    | 1154156    | CLOSED_ERRATA          | sat-6.1.0+             | 312 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    bz_bug_is_open    | 1096333    | CLOSED_ERRATA          | sat-6.1.0+, sat-6.0.z+ | 352 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    bz_bug_is_open    | 1187366    | CLOSED_CURRENTRELEASE  | sat-6.1.1+             | 360 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    bz_bug_is_open    | 1154156    | CLOSED_ERRATA          | sat-6.1.0+             | 406 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    bz_bug_is_open    | 1154156    | CLOSED_ERRATA          | sat-6.1.0+             | 448 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    bz_bug_is_open    | 1096333    | CLOSED_ERRATA          | sat-6.1.0+, sat-6.0.z+ | 478 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    bz_bug_is_open    | 1187366    | CLOSED_CURRENTRELEASE  | sat-6.1.1+             | 481 -> ../robottelo-fork/tests/foreman/api/test_multiple_paths.py
    skip_if_bug_open  | 1230902    | CLOSED_WONTFIX         | sat-backlog+           | 122 -> ../robottelo-fork/tests/foreman/api/test_operatingsystem.py
    skip_if_bug_open  | 1328935    | VERIFIED               | sat-6.3.0+             | 308 -> ../robottelo-fork/tests/foreman/api/test_operatingsystem.py
    skip_if_bug_open  | 1230865    | NEW                    | sat-backlog+           | 288 -> ../robottelo-fork/tests/foreman/api/test_organization.py
    skip_if_bug_open  | 1103157    | CLOSED_WONTFIX         | sat-backlog+           | 412 -> ../robottelo-fork/tests/foreman/api/test_organization.py
    skip_if_bug_open  | 1229384    | CLOSED_ERRATA          | sat-6.2.0+             | 37 -> ../robottelo-fork/tests/foreman/api/test_partitiontable.py
    skip_if_bug_open  | 1310422    | NEW                    | sat-backlog?           | 232 -> ../robottelo-fork/tests/foreman/api/test_product.py
    skip_if_bug_open  | 1311113    | NEW                    | sat-backlog?           | 697 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 773 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 802 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 830 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    skip_if_bug_open  | 1194476    | NEW                    | sat-backlog+           | 997 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    skip_if_bug_open  | 1378442    | NEW                    | sat-backlog?           | 1026 -> ../robottelo-fork/tests/foreman/api/test_repository.py
    bz_bug_is_open    | 1112657    | CLOSED_ERRATA          | sat-6.1.0+             | 42 -> ../robottelo-fork/tests/foreman/api/test_role.py
    bz_bug_is_open    | 1112657    | CLOSED_ERRATA          | sat-6.1.0+             | 57 -> ../robottelo-fork/tests/foreman/api/test_role.py
    bz_bug_is_open    | 1112657    | CLOSED_ERRATA          | sat-6.1.0+             | 76 -> ../robottelo-fork/tests/foreman/api/test_role.py
    skip_if_bug_open  | 1398695    | POST                   | sat-6.3.0?             | 85 -> ../robottelo-fork/tests/foreman/api/test_smartproxy.py
    skip_if_bug_open  | 1199150    | NEW                    | sat-backlog?           | 458 -> ../robottelo-fork/tests/foreman/api/test_syncplan.py
    skip_if_bug_open  | 1199150    | NEW                    | sat-backlog?           | 511 -> ../robottelo-fork/tests/foreman/api/test_syncplan.py
    skip_if_bug_open  | 1202564    | CLOSED_CURRENTRELEASE  | sat-6.1.0+             | 32 -> ../robottelo-fork/tests/foreman/api/test_template.py
    skip_if_bug_open  | 1110476    | NEW                    | sat-backlog?           | 565 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1360239    | ON_QA                  | sat-6.3.0+, sat-6.2.z+ | 625 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1360239    | ON_QA                  | sat-6.3.0+, sat-6.2.z+ | 649 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1339211    | CLOSED_ERRATA          | sat-6.2.0+             | 708 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1336716    | CLOSED_ERRATA          | sat-6.2.z+             | 873 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1336716    | CLOSED_ERRATA          | sat-6.2.z+             | 913 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1360239    | ON_QA                  | sat-6.3.0+, sat-6.2.z+ | 1171 -> ../robottelo-fork/tests/foreman/cli/test_activationkey.py
    skip_if_bug_open  | 1398695    | POST                   | sat-6.3.0?             | 79 -> ../robottelo-fork/tests/foreman/cli/test_capsule.py
    skip_if_bug_open  | 1357864    | VERIFIED               | sat-6.3.0+             | 380 -> ../robottelo-fork/tests/foreman/cli/test_classparameters.py
    skip_if_bug_open  | 1214312    | CLOSED_WONTFIX         | sat-backlog+           | 253 -> ../robottelo-fork/tests/foreman/cli/test_computeresource.py
    skip_if_bug_open  | 1328202    | CLOSED_ERRATA          | sat-6.2.0+             | 278 -> ../robottelo-fork/tests/foreman/cli/test_contenthost.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 210 -> ../robottelo-fork/tests/foreman/cli/test_contentview.py
    skip_if_bug_open  | 1317057    | CLOSED_ERRATA          | sat-6.2.0+             | 269 -> ../robottelo-fork/tests/foreman/cli/test_contentview.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 684 -> ../robottelo-fork/tests/foreman/cli/test_contentview.py
    skip_if_bug_open  | 1343006    | CLOSED_ERRATA          | sat-6.2.0+             | 764 -> ../robottelo-fork/tests/foreman/cli/test_contentview.py
    skip_if_bug_open  | 1359665    | CLOSED_ERRATA          | sat-6.2.z+             | 1607 -> ../robottelo-fork/tests/foreman/cli/test_contentview.py
    skip_if_bug_open  | 1236532    | CLOSED_ERRATA          | sat-6.2.0+             | 139 -> ../robottelo-fork/tests/foreman/cli/test_contentviewfilter.py
    skip_if_bug_open  | 1356906    | VERIFIED               | sat-6.3.0+             | 165 -> ../robottelo-fork/tests/foreman/cli/test_contentviewfilter.py
    skip_if_bug_open  | 1343006    | CLOSED_ERRATA          | sat-6.2.0+             | 264 -> ../robottelo-fork/tests/foreman/cli/test_contentviewfilter.py
    bz_bug_is_open    | 1328943    | CLOSED_ERRATA          | sat-6.2.0+             | 651 -> ../robottelo-fork/tests/foreman/cli/test_contentviewfilter.py
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
    skip_if_bug_open  | 1269208    | NEW                    | sat-backlog+           | 1582 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    skip_if_bug_open  | 1230915    | CLOSED_ERRATA          | sat-6.1.z+             | 1641 -> ../robottelo-fork/tests/foreman/cli/test_docker.py
    bz_bug_is_open    | 1398392    | POST                   | sat-6.3.0?, sat-6.2.z? | 50 -> ../robottelo-fork/tests/foreman/cli/test_domain.py
    bz_bug_is_open    | 1398392    | POST                   | sat-6.3.0?, sat-6.2.z? | 77 -> ../robottelo-fork/tests/foreman/cli/test_domain.py
    skip_if_bug_open  | 1405428    | CLOSED_DUPLICATE       | sat-6.3.0?, sat-6.2.z? | 83 -> ../robottelo-fork/tests/foreman/cli/test_errata.py
         DUPLICATE OF:
         - 1372372    - MODIFIED               - sat-6.2.z+
    skip_if_bug_open  | 1402767    | CLOSED_DUPLICATE       |                        | 1043 -> ../robottelo-fork/tests/foreman/cli/test_errata.py
         DUPLICATE OF:
         - 1283173    - CLOSED_ERRATA          - sat-6.2.0+
    bz_bug_is_open    | 1219610    | CLOSED_WONTFIX         | sat-backlog+           | 100 -> ../robottelo-fork/tests/foreman/cli/test_hammer.py
    bz_bug_is_open    | 1219610    | CLOSED_WONTFIX         | sat-backlog+           | 121 -> ../robottelo-fork/tests/foreman/cli/test_hammer.py
    skip_if_bug_open  | 1328925    | CLOSED_ERRATA          | sat-6.2.0+             | 185 -> ../robottelo-fork/tests/foreman/cli/test_host_collection.py
    skip_if_bug_open  | 1328925    | CLOSED_ERRATA          | sat-6.2.0+             | 207 -> ../robottelo-fork/tests/foreman/cli/test_host_collection.py
    skip_if_bug_open  | 1245334    | CLOSED_WONTFIX         | sat-backlog+           | 228 -> ../robottelo-fork/tests/foreman/cli/test_host_collection.py
    skip_if_bug_open  | 1328925    | CLOSED_ERRATA          | sat-6.2.0+             | 252 -> ../robottelo-fork/tests/foreman/cli/test_host_collection.py
    skip_if_bug_open  | 1354544    | CLOSED_CURRENTRELEASE  | sat-backlog?           | 189 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
    skip_if_bug_open  | 1313056    | NEW                    | sat-backlog?           | 218 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
    skip_if_bug_open  | 1354568    | POST                   | sat-backlog?           | 362 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
    skip_if_bug_open  | 1354568    | POST                   | sat-backlog?           | 385 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
    skip_if_bug_open  | 1354568    | POST                   | sat-backlog?           | 408 -> ../robottelo-fork/tests/foreman/cli/test_hostgroup.py
    skip_if_bug_open  | 1325880    | CLOSED_ERRATA          | sat-6.2.0+             | 1310 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    bz_bug_is_open    | 1226981    | CLOSED_ERRATA          | sat-6.1.z+             | 1379 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1238247    | NEW                    | sat-backlog?           | 1524 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1238247    | NEW                    | sat-backlog?           | 1555 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1238247    | NEW                    | sat-backlog?           | 1596 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1267224    | CLOSED_WONTFIX         | sat-backlog+           | 1597 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1325880    | CLOSED_ERRATA          | sat-6.2.0+             | 1667 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1325880    | CLOSED_ERRATA          | sat-6.2.0+             | 1707 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1325124    | CLOSED_ERRATA          | sat-6.2.0+             | 1763 -> ../robottelo-fork/tests/foreman/cli/test_import.py
    skip_if_bug_open  | 1233612    | VERIFIED               | sat-6.3.0+             | 79 -> ../robottelo-fork/tests/foreman/cli/test_location.py
    skip_if_bug_open  | 1234287    | POST                   | sat-6.2.z+             | 314 -> ../robottelo-fork/tests/foreman/cli/test_location.py
    skip_if_bug_open  | 1229384    | CLOSED_ERRATA          | sat-6.2.0+             | 29 -> ../robottelo-fork/tests/foreman/cli/test_partitiontable.py
    bz_bug_is_open    | 1219490    | CLOSED_WONTFIX         | sat-backlog+           | 319 -> ../robottelo-fork/tests/foreman/cli/test_product.py
    skip_if_bug_open  | 1283173    | CLOSED_ERRATA          | sat-6.2.0+             | 45 -> ../robottelo-fork/tests/foreman/cli/test_puppetmodule.py
    skip_if_bug_open  | 1103944    | CLOSED_WORKSFORME      | sat-6.2.0+             | 407 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 678 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 709 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1328092    | CLOSED_ERRATA          | sat-6.2.z+             | 742 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1343006    | CLOSED_ERRATA          | sat-6.2.0+             | 962 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1378442    | NEW                    | sat-backlog?           | 996 -> ../robottelo-fork/tests/foreman/cli/test_repository.py
    skip_if_bug_open  | 1226425    | CLOSED_WONTFIX         | sat-backlog+           | 169 -> ../robottelo-fork/tests/foreman/cli/test_subscription.py
    skip_if_bug_open  | 1336790    | CLOSED_ERRATA          | sat-6.2.0+             | 275 -> ../robottelo-fork/tests/foreman/cli/test_syncplan.py
    skip_if_bug_open  | 1138553    | CLOSED_ERRATA          | sat-6.2.0+             | 158 -> ../robottelo-fork/tests/foreman/cli/test_user.py
    skip_if_bug_open  | 1138553    | CLOSED_ERRATA          | sat-6.2.0+             | 183 -> ../robottelo-fork/tests/foreman/cli/test_user.py
    skip_if_bug_open  | 1204686    | CLOSED_WONTFIX         | sat-backlog?           | 372 -> ../robottelo-fork/tests/foreman/cli/test_user.py
    skip_if_bug_open  | 1204667    | POST                   | sat-6.4.0+             | 854 -> ../robottelo-fork/tests/foreman/cli/test_user.py
    bz_bug_is_open    | 1166875    | NEW                    | sat-backlog?           | 822 -> ../robottelo-fork/tests/foreman/endtoend/test_api_endtoend.py
    bz_bug_is_open    | 1328202    | CLOSED_ERRATA          | sat-6.2.0+             | 357 -> ../robottelo-fork/tests/foreman/endtoend/test_cli_endtoend.py
    bz_bug_is_open    | 1191422    | CLOSED_ERRATA          | sat-6.1.0+             | 400 -> ../robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py
    bz_bug_is_open    | 1191422    | CLOSED_ERRATA          | sat-6.1.0+             | 409 -> ../robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py
    bz_bug_is_open    | 1191422    | CLOSED_ERRATA          | sat-6.1.0+             | 416 -> ../robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py
    bz_bug_is_open    | 1191541    | CLOSED_CURRENTRELEASE  | sat-6.1.0+             | 433 -> ../robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py
    bz_bug_is_open    | 1246152    | CLOSED_ERRATA          | sat-6.2.0+             | 100 -> ../robottelo-fork/tests/foreman/installer/test_installer.py
    skip_if_bug_open  | 1259057    | CLOSED_ERRATA          | sat-6.1.z+             | 297 -> ../robottelo-fork/tests/foreman/longrun/test_inc_updates.py
    skip_if_bug_open  | 1342057    | VERIFIED               | sat-6.3.0+, sat-6.2.z+ | 1158 -> ../robottelo-fork/tests/foreman/ui/test_activationkey.py
    skip_if_bug_open  | 1326633    | NEW                    | sat-backlog+           | 226 -> ../robottelo-fork/tests/foreman/ui/test_bookmark.py
    skip_if_bug_open  | 1324484    | CLOSED_ERRATA          | sat-6.2.0+             | 453 -> ../robottelo-fork/tests/foreman/ui/test_bookmark.py
    skip_if_bug_open  | 1324484    | CLOSED_ERRATA          | sat-6.2.0+             | 493 -> ../robottelo-fork/tests/foreman/ui/test_bookmark.py
    skip_if_bug_open  | 1295179    | CLOSED_ERRATA          | sat-6.2.0+             | 1166 -> ../robottelo-fork/tests/foreman/ui/test_classparameters.py
    skip_if_bug_open  | 1402826    | CLOSED_DUPLICATE       | sat-6.2.z?             | 759 -> ../robottelo-fork/tests/foreman/ui/test_contentview.py
         DUPLICATE OF:
         - 981639     - VERIFIED               - sat-6.3.0+
    skip_if_bug_open  | 1308831    | VERIFIED               | sat-6.3.0+             | 280 -> ../robottelo-fork/tests/foreman/ui/test_discoveryrule.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1437 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1461 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1490 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1518 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1547 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1333805    | CLOSED_ERRATA          | sat-6.2.0+             | 1576 -> ../robottelo-fork/tests/foreman/ui/test_docker.py
    skip_if_bug_open  | 1123360    | CLOSED_ERRATA          | sat-6.1.0+             | 265 -> ../robottelo-fork/tests/foreman/ui/test_domain.py
    skip_if_bug_open  | 1210180    | CLOSED_WONTFIX         | sat-backlog+           | 727 -> ../robottelo-fork/tests/foreman/ui/test_gpgkey.py
    skip_if_bug_open  | 1210180    | CLOSED_WONTFIX         | sat-backlog+           | 1013 -> ../robottelo-fork/tests/foreman/ui/test_gpgkey.py
    skip_if_bug_open  | 1210180    | CLOSED_WONTFIX         | sat-backlog+           | 1324 -> ../robottelo-fork/tests/foreman/ui/test_gpgkey.py
    skip_if_bug_open  | 1300350    | NEW                    | sat-backlog?           | 136 -> ../robottelo-fork/tests/foreman/ui/test_hostcollection.py
    skip_if_bug_open  | 1394974    | NEW                    | sat-6.2.z?             | 93 -> ../robottelo-fork/tests/foreman/ui/test_navigation.py
    skip_if_bug_open  | 1328935    | VERIFIED               | sat-6.3.0+             | 142 -> ../robottelo-fork/tests/foreman/ui/test_operatingsystem.py
    skip_if_bug_open  | 1079482    | CLOSED_WONTFIX         | sat-backlog+           | 156 -> ../robottelo-fork/tests/foreman/ui/test_organization.py
    skip_if_bug_open  | 1289571    | ON_QA                  | sat-6.3.0+             | 70 -> ../robottelo-fork/tests/foreman/ui/test_oscapcontent.py
    skip_if_bug_open  | 1293296    | ON_QA                  | sat-6.3.0+             | 116 -> ../robottelo-fork/tests/foreman/ui/test_oscappolicy.py
    bz_bug_is_open    | 1335799    | CLOSED_ERRATA          | sat-6.2.0+             | 43 -> ../robottelo-fork/tests/foreman/ui/test_setting.py
    skip_if_bug_open  | 1125181    | CLOSED_ERRATA          | sat-6.2.0+             | 220 -> ../robottelo-fork/tests/foreman/ui/test_setting.py
    skip_if_bug_open  | 1125181    | CLOSED_ERRATA          | sat-6.2.0+             | 336 -> ../robottelo-fork/tests/foreman/ui/test_setting.py
    skip_if_bug_open  | 1156195    | CLOSED_CURRENTRELEASE  | sat-backlog+           | 366 -> ../robottelo-fork/tests/foreman/ui/test_setting.py
    skip_if_bug_open  | 1259174    | CLOSED_ERRATA          | sat-6.2.0+             | 528 -> ../robottelo-fork/tests/foreman/ui/test_variables.py
    parse time:257.0 seconds









