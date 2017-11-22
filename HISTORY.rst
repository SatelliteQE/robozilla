=======
History
=======

0.2.2 (2017-11-22)
------------------
* Follow DUPLICATE status if BZ is CLOSED DUPLICATE 
* Fix infinite loops when circular referenced BZ is decorated
* Added more status_resolution to BZ_CLOSED_STATUSES
* On decorators follow_duplicates will default to True (but will follow only for status DUPLICATE)

0.2.1 (2017-10-17)
------------------
* Added default pickers to get version and config from environment variables

0.2.0 (2017-07-25)
------------------
* Added decorator for pytest parametrized tests

0.1.8 (2017-03-02)
------------------
* implement subcommands scan and coverage
* implement coverage stats

0.1.7 (2017-02-14)
------------------
* Handle None bug returned when missing bugzilla credentials
* Better handle credentials when set in environment

0.1.6 (2017-02-10)
------------------
* First official release.
