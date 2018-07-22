# _*_ coding: utf-8 _*_
import sys
from os import path
import unittest

import pycodestyle

from lw301_server_tests import PROJECT_ROOT

_src_dirs = [path.join(PROJECT_ROOT, 'lw301_server'),
             path.join(PROJECT_ROOT, 'lw301_server_tests'),
             path.join(PROJECT_ROOT, 'setup.py')]


class StyleTestCase(unittest.TestCase):

    def test_pycodestyle(self):
        pep8style = pycodestyle.StyleGuide(
            show_pep8=False,
            show_source=True,
            repeat=True,
            max_line_length=120,
            statistics=True,
        )
        result = pep8style.check_files(_src_dirs)

        if result.total_errors > 0:
            sys.stderr.write('Statistics:\n{}\n'.format(result.get_statistics('')))
            self.fail('PEP8 styles errors')
