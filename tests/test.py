import logging
import unittest

import nfw

log = logging.getLogger(__name__)

if __name__ == "__main__":
    alltests = unittest.TestLoader().discover('tests',pattern='*.py')
    unittest.TextTestRunner(verbosity=2).run(alltests)
