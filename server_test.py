#!/usr/bin/env python3
"""This file runs a suite of unit tests on the fStream application logging timestamped output in 'tests.log' file.  """

import logging
import unittest


class TestFStream(unittest.TestCase):
    """This class has methods that run unit tests on the FStream() application."""

    @classmethod
    def setUpClass(cls):
        """Set up logging for unit test.

        During testing, events are logged in the 'tests.log' file in the following format:
        YYYY-MM-DD hh:mm:ss,ms LOG-LEVEL MESSAGE
        In addition, the name of this testing file is logged.
        """

        logging.basicConfig(
            filename="tests.log",
            format="%(asctime)s,%(msecs)03d %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info("test_get_cookies.py")

    @classmethod
    def tearDownClass(cls):
        """Log exit message with a line break to separate successive runs of the program."""

        logging.info("Tests complete. Exiting\n" + "-" * 70)

    def setUp(self):
        """ """

        return


    def test_always_passes(self):
        """This test will always pass."""

        self.assertEqual(True, True)

if __name__ == "__main__":
    unittest.main()