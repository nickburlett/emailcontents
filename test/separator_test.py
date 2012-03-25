from base import BaseTest
from emailcontents.quoted import extract

sample1 = """\
foo
============
bar
============
baz
"""

sample2 = """\
foo
> bar
> ============
> baz
> ============
"""

class SeparatorTest(BaseTest):
    def sample1_test(self):
        "Ensure separators work"
        x = [
            {'text' : 'foo', 'quoter' : '', 'raw' : 'foo'},
            {'text' : '============', 'quoter' : '', 'raw' : '============', 'separator' : 1 },
            {'text' : 'bar', 'quoter' : '', 'raw' : 'bar'},
            {'text' : '============', 'quoter' : '', 'raw' : '============', 'separator' : 1 },
            {'text' : 'baz', 'quoter' : '', 'raw' : 'baz'},
            ]
        x = self._massage(x)
        self.assertEquals( extract(sample1), x )

    def sample2_test(self):
        "Separators should work in quoted areas"
        x = [
            {'text' : 'foo', 'quoter' : '', 'raw' : 'foo'},
            [
                {'text' : 'bar', 'quoter' : '>', 'raw' : '> bar'},
                {'text' : '============', 'quoter' : '>', 'raw' : '> ============', 'separator' : 1 },
                {'text' : 'baz', 'quoter' : '>', 'raw' : '> baz'},
                {'text' : '============', 'quoter' : '>', 'raw' : '> ============', 'separator' : 1 },
            ],
            ]
        x = self._massage(x)
        self.assertEquals( extract(sample2), x )

