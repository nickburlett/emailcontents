import unittest

class BaseTest(unittest.TestCase):
    def _massage(self, x):
        if isinstance(x, dict):
            x['separator'] = x.get('separator', False)
            if x['separator'] :
                x['separator'] = True
            x['empty'] = x.get('empty', False)
            if x['empty']:
                x['empty'] = True
            return x
        elif isinstance(x, list):
            return [self._massage(n) for n in x]

