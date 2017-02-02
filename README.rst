Robottelo Bugzilla Parser
=========================

This is an early stage version

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

    (2.7) dlezz@elysion:~/projects/robottelo_bz_parse$ ./start.sh
    ./parse.py
    /home/dlezz/projects/robottelo_bz_parse
    /home/dlezz/projects/robottelo_bz_parse/output
    found bz usage: BZDecorator 1295179 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_classparameters.py line: 1166
    found bz usage: BZDecorator 1293296 ON_QA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_oscappolicy.py line: 116
    found bz usage: BZDecorator 1342057 VERIFIED /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_activationkey.py line: 1158
    found bz usage: BZDecorator 1326633 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_bookmark.py line: 226
    found bz usage: BZDecorator 1324484 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_bookmark.py line: 453
    found bz usage: BZDecorator 1324484 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_bookmark.py line: 493
    found bz usage: BZDecorator 1210180 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_gpgkey.py line: 727
    found bz usage: BZDecorator 1210180 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_gpgkey.py line: 1013
    found bz usage: BZDecorator 1210180 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_gpgkey.py line: 1324
    found bz usage: BZDecorator 1333805 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_docker.py line: 1437
    found bz usage: BZDecorator 1333805 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_docker.py line: 1461
    found bz usage: BZDecorator 1333805 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_docker.py line: 1490
    found bz usage: BZDecorator 1333805 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_docker.py line: 1518
    found bz usage: BZDecorator 1333805 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_docker.py line: 1547
    found bz usage: BZDecorator 1333805 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_docker.py line: 1576
    found bz usage: BZDecorator 1079482 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_organization.py line: 156
    found bz usage: BZDecorator 1328935 VERIFIED /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_operatingsystem.py line: 142
    found bz usage: BZDecorator 1123360 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_domain.py line: 265
    found bz usage: BZDecorator 1308831 VERIFIED /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_discoveryrule.py line: 280
    found bz usage: BZDecorator 1259174 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_variables.py line: 528
    found bz usage: BZIsOpen 1335799 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_setting.py line: 43
    found bz usage: BZDecorator 1125181 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_setting.py line: 220
    found bz usage: BZDecorator 1125181 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_setting.py line: 336
    found bz usage: BZDecorator 1156195 CLOSED_CURRENTRELEASE /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_setting.py line: 366
    found bz usage: BZDecorator 1402826 CLOSED_DUPLICATE /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_contentview.py line: 754
    found bz usage: BZDecorator 1300350 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_hostcollection.py line: 136
    found bz usage: BZDecorator 1289571 ON_QA /home/dlezz/projects/robottelo-fork/tests/foreman/ui/test_oscapcontent.py line: 70
    found bz usage: BZDecorator 1259057 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/longrun/test_inc_updates.py line: 297
    found bz usage: BZDecorator 1311113 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_repository.py line: 697
    found bz usage: BZDecorator 1328092 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_repository.py line: 773
    found bz usage: BZDecorator 1328092 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_repository.py line: 802
    found bz usage: BZDecorator 1328092 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_repository.py line: 830
    found bz usage: BZDecorator 1194476 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_repository.py line: 997
    found bz usage: BZDecorator 1378442 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_repository.py line: 1026
    found bz usage: BZDecorator 1199150 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_syncplan.py line: 458
    found bz usage: BZDecorator 1199150 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_syncplan.py line: 511
    found bz usage: BZDecorator 1156555 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_activationkey.py line: 126
    found bz usage: BZDecorator 1217635 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_docker.py line: 608
    found bz usage: BZDecorator 1282431 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_docker.py line: 1231
    found bz usage: BZDecorator 1230865 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_organization.py line: 288
    found bz usage: BZDecorator 1103157 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_organization.py line: 412
    found bz usage: BZDecorator 1310422 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_product.py line: 232
    found bz usage: BZDecorator 1230902 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_operatingsystem.py line: 122
    found bz usage: BZDecorator 1328935 VERIFIED /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_operatingsystem.py line: 308
    found bz usage: BZDecorator 1398695 POST /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_smartproxy.py line: 85
    found bz usage: BZDecorator 1262037 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_smartproxy.py line: 237
    found bz usage: BZIsOpen 1118015 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_multiple_paths.py line: 233
    found bz usage: BZDecorator 1122257 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_multiple_paths.py line: 244
    found bz usage: BZIsOpen 1154156 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_multiple_paths.py line: 312
    found bz usage: BZIsOpen 1096333 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_multiple_paths.py line: 352
    found bz usage: BZIsOpen 1187366 CLOSED_CURRENTRELEASE /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_multiple_paths.py line: 360
    found bz usage: BZIsOpen 1154156 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_multiple_paths.py line: 406
    found bz usage: BZIsOpen 1154156 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_multiple_paths.py line: 448
    found bz usage: BZIsOpen 1096333 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_multiple_paths.py line: 478
    found bz usage: BZIsOpen 1187366 CLOSED_CURRENTRELEASE /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_multiple_paths.py line: 481
    found bz usage: BZDecorator 1262029 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_environment.py line: 222
    found bz usage: BZDecorator 1242534 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_contentviewfilter.py line: 647
    found bz usage: BZDecorator 1222118 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_hostgroup.py line: 46
    found bz usage: BZIsOpen 1112657 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_role.py line: 42
    found bz usage: BZIsOpen 1112657 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_role.py line: 57
    found bz usage: BZIsOpen 1112657 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_role.py line: 76
    found bz usage: BZIsOpen 1223494 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_contentview.py line: 99
    found bz usage: BZDecorator 1297308 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_contentview.py line: 176
    found bz usage: BZDecorator 1147100 ASSIGNED /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_contentview.py line: 991
    found bz usage: BZDecorator 1302725 VERIFIED /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_bookmarks.py line: 199
    found bz usage: BZDecorator 1349364 VERIFIED /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_discoveredhost.py line: 129
    found bz usage: BZIsOpen 1392919 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_discoveredhost.py line: 148
    found bz usage: BZDecorator 1415679 POST /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_hostcollection.py line: 55
    found bz usage: BZDecorator 1325989 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_hostcollection.py line: 142
    found bz usage: BZDecorator 1325989 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_hostcollection.py line: 158
    found bz usage: BZDecorator 1325989 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_hostcollection.py line: 174
    found bz usage: BZDecorator 1325989 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_hostcollection.py line: 192
    found bz usage: BZDecorator 1325989 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_hostcollection.py line: 210
    found bz usage: BZDecorator 1229384 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_partitiontable.py line: 37
    found bz usage: BZDecorator 1202564 CLOSED_CURRENTRELEASE /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_template.py line: 32
    found bz usage: BZIsOpen 1203865 POST /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_host.py line: 88
    found bz usage: BZIsOpen 1210001 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/api/test_host.py line: 105
    found bz usage: BZIsOpen 1191422 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py line: 400
    found bz usage: BZIsOpen 1191422 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py line: 409
    found bz usage: BZIsOpen 1191422 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py line: 416
    found bz usage: BZIsOpen 1191541 CLOSED_CURRENTRELEASE /home/dlezz/projects/robottelo-fork/tests/foreman/endtoend/test_ui_endtoend.py line: 433
    found bz usage: BZIsOpen 1328202 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/endtoend/test_cli_endtoend.py line: 357
    found bz usage: BZIsOpen 1166875 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/endtoend/test_api_endtoend.py line: 822
    found bz usage: BZIsOpen 1246152 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/installer/test_installer.py line: 100
    found bz usage: BZDecorator 1103944 CLOSED_WORKSFORME /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_repository.py line: 407
    found bz usage: BZDecorator 1328092 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_repository.py line: 678
    found bz usage: BZDecorator 1328092 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_repository.py line: 709
    found bz usage: BZDecorator 1328092 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_repository.py line: 742
    found bz usage: BZDecorator 1343006 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_repository.py line: 962
    found bz usage: BZDecorator 1378442 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_repository.py line: 996
    found bz usage: BZDecorator 1357864 VERIFIED /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_classparameters.py line: 380
    found bz usage: BZDecorator 1325880 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_import.py line: 1310
    found bz usage: BZIsOpen 1226981 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_import.py line: 1379
    found bz usage: BZDecorator 1238247 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_import.py line: 1524
    found bz usage: BZDecorator 1238247 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_import.py line: 1555
    found bz usage: BZDecorator 1238247 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_import.py line: 1596
    found bz usage: BZDecorator 1267224 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_import.py line: 1597
    found bz usage: BZDecorator 1325880 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_import.py line: 1667
    found bz usage: BZDecorator 1325880 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_import.py line: 1707
    found bz usage: BZDecorator 1325124 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_import.py line: 1763
    found bz usage: BZDecorator 1336790 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_syncplan.py line: 275
    found bz usage: BZDecorator 1110476 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_activationkey.py line: 565
    found bz usage: BZDecorator 1360239 ON_QA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_activationkey.py line: 625
    found bz usage: BZDecorator 1360239 ON_QA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_activationkey.py line: 649
    found bz usage: BZDecorator 1339211 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_activationkey.py line: 708
    found bz usage: BZDecorator 1336716 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_activationkey.py line: 873
    found bz usage: BZDecorator 1336716 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_activationkey.py line: 913
    found bz usage: BZDecorator 1360239 ON_QA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_activationkey.py line: 1171
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 476
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 511
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 584
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 658
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 776
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 835
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 1007
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 1063
    found bz usage: BZDecorator 1282431 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 1496
    found bz usage: BZDecorator 1230915 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 1547
    found bz usage: BZDecorator 1269196 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 1548
    found bz usage: BZDecorator 1230915 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 1581
    found bz usage: BZDecorator 1269208 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 1582
    found bz usage: BZDecorator 1230915 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_docker.py line: 1641
    found bz usage: BZDecorator 1138553 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_user.py line: 158
    found bz usage: BZDecorator 1138553 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_user.py line: 183
    found bz usage: BZDecorator 1204686 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_user.py line: 372
    found bz usage: BZDecorator 1204667 POST /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_user.py line: 854
    found bz usage: BZDecorator 1233612 VERIFIED /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_location.py line: 79
    found bz usage: BZDecorator 1234287 POST /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_location.py line: 314
    found bz usage: BZIsOpen 1219490 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_product.py line: 319
    found bz usage: BZIsOpen 1398392 POST /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_domain.py line: 50
    found bz usage: BZIsOpen 1398392 POST /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_domain.py line: 77
    found bz usage: BZDecorator 1226425 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_subscription.py line: 169
    found bz usage: BZDecorator 1214312 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_computeresource.py line: 253
    found bz usage: BZDecorator 1405428 CLOSED_DUPLICATE /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_errata.py line: 83
    found bz usage: BZDecorator 1402767 CLOSED_DUPLICATE /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_errata.py line: 1043
    found bz usage: BZDecorator 1236532 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_contentviewfilter.py line: 139
    found bz usage: BZDecorator 1356906 VERIFIED /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_contentviewfilter.py line: 165
    found bz usage: BZDecorator 1343006 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_contentviewfilter.py line: 264
    found bz usage: BZIsOpen 1328943 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_contentviewfilter.py line: 651
    found bz usage: BZIsOpen 1219610 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_hammer.py line: 100
    found bz usage: BZIsOpen 1219610 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_hammer.py line: 121
    found bz usage: BZDecorator 1328925 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_host_collection.py line: 185
    found bz usage: BZDecorator 1328925 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_host_collection.py line: 207
    found bz usage: BZDecorator 1245334 CLOSED_WONTFIX /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_host_collection.py line: 228
    found bz usage: BZDecorator 1328925 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_host_collection.py line: 252
    found bz usage: BZDecorator 1354544 CLOSED_CURRENTRELEASE /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_hostgroup.py line: 189
    found bz usage: BZDecorator 1313056 NEW /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_hostgroup.py line: 218
    found bz usage: BZDecorator 1354568 POST /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_hostgroup.py line: 362
    found bz usage: BZDecorator 1354568 POST /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_hostgroup.py line: 385
    found bz usage: BZDecorator 1354568 POST /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_hostgroup.py line: 408
    found bz usage: BZDecorator 1328202 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_contenthost.py line: 278
    found bz usage: BZDecorator 1283173 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_puppetmodule.py line: 45
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_contentview.py line: 210
    found bz usage: BZDecorator 1317057 NONE /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_contentview.py line: 269
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_contentview.py line: 684
    found bz usage: BZDecorator 1343006 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_contentview.py line: 764
    found bz usage: BZDecorator 1359665 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_contentview.py line: 1607
    found bz usage: BZDecorator 1398695 POST /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_capsule.py line: 80
    found bz usage: BZDecorator 1229384 CLOSED_ERRATA /home/dlezz/projects/robottelo-fork/tests/foreman/cli/test_partitiontable.py line: 29
    parse time:94.0 seconds








