from unittest import TestCase

import phred

class TestPhred(TestCase):
    def test_is_string(self):
        s = 'funniest.joke()'
        self.assertTrue( isinstance( s, str ) )
