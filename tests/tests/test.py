import logging
import unittest

import nfw

log = logging.getLogger(__name__)

class Testing(unittest.TestCase):
    def testing(self):
        self.assertEqual('foo', 'foo')
