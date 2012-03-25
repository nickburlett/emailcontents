from emailcontents.quoted import extract
from base import BaseTest

a = """\
> foo
> # Bar
> baz

quux
"""


b = """\

> foo
> > > baz
> > quux
> quuux
quuuux
"""

c = """\
> a
>> b
> c
"""

d = """\
>
cpan>
>
"""

e = """\
> a
cpan > b
> c
"""

f = """\
> a

=> b

> c
"""

g = """\
> a
=> b
> c
"""

class Test(BaseTest):
    #maxDiff = 1000


    def test_a(self):
        "Sample text is organized properly"
        x = [[{'text' : 'foo','quoter' : '>','raw' : '> foo', 'empty': False, 'separator': False},
              [{'text' : 'Bar','quoter' : '> #','raw' : '> # Bar', 'empty':False, 'separator': False}],
               {'text' : 'baz','quoter' : '>','raw' : '> baz', 'empty':False, 'separator': False}
              ],
             {'text' : '','empty' : True,'quoter' : '','raw' : '', 'separator': False},
             {'text' : 'quux','quoter' : '','raw' : 'quux', 'empty':False, 'separator': False}
            ]
        self.assertEqual( extract(a) , x )

    def test_b(self):
        "Skipping levels works okay"
        x = [
              { 'text' : '', 'empty' : '1', 'quoter' : '', 'raw' : '' },
              [
                { 'text' : 'foo', 'quoter' : '>', 'raw' : '> foo' },
                [
                  [
                    { 'text' : 'baz', 'quoter' : '> > >',
                      'raw' : '> > > baz' }
                  ],
                  { 'text' : 'quux', 'quoter' : '> >', 'raw' : '> > quux' }
                ],
                { 'text' : 'quuux', 'quoter' : '>', 'raw' : '> quuux' }
              ],
              { 'text' : 'quuuux', 'quoter' : '', 'raw' : 'quuuux' }
            ];
        x = self._massage(x)
        self.assertEqual( extract(b), x )

    def test_c(self):
        "correctly parse >> delimiter"
        x= [ 
             { 'text' : 'a', 'quoter' : '>', 'raw' : '> a' },
             [ { 'text' : 'b', 'quoter' : '>>', 'raw' : '>> b' } ],
             { 'text' : 'c', 'quoter' : '>', 'raw' : '> c' }
           ]
        x = self._massage(x)
        self.assertEqual( extract(c), x )

    def test_d(self):
        "correctly parse cpan> delimiter with no text"
        x = [
               [ { 'text' : '', 'empty' : 1, 'quoter' : '>', 'raw' : '>' } ],
               [ { 'text' : '', 'empty' : 1, 'quoter' : 'cpan>', 'raw' : 'cpan>' } ],
               [ { 'text' : '', 'empty' : 1, 'quoter' : '>', 'raw' : '>' } ]
            ]
        x = self._massage(x)
        self.assertEqual( extract(d), x )


    def test_e(self):
        "correctly handles a non-delimiter"
        x = [
               [ { 'text' : 'a', 'quoter' : '>', 'raw' : '> a' } ],
               { 'text' : 'cpan > b', 'quoter' : '', 'raw' : 'cpan > b' },
               [ { 'text' : 'c', 'quoter' : '>', 'raw' : '> c' } ],
            ]
        x = self._massage(x)
        self.assertEqual( extract(e), x )

    def test_f(self):
        "correctly parse => delimiter with blank lines"
        x = [
               [ { 'text' : 'a', 'quoter' : '>', 'raw' : '> a' } ],
               { 'text' : '', 'empty' : 1, 'quoter' : '', 'raw' : '' },
               [ { 'text' : 'b', 'quoter' : '=>', 'raw' : '=> b' } ],
               { 'text' : '', 'empty' : 1, 'quoter' : '', 'raw' : '' },
               [ { 'text' : 'c', 'quoter' : '>', 'raw' : '> c' } ]
            ]
        x = self._massage(x)
        self.assertEqual( extract(f), x )

    def test_g(self):
        "correctly parse => delimiter"
        x = [
               [ { 'text' : 'a', 'quoter' : '>', 'raw' : '> a' } ],
               [ { 'text' : 'b', 'quoter' : '=>', 'raw' : '=> b' } ],
               [ { 'text' : 'c', 'quoter' : '>', 'raw' : '> c' } ]
            ]
        x = self._massage(x)
        self.assertEqual( extract(g), x )

    def test_g(self):
        "correctly parse => delimiter"
        x = [
               [ { 'text' : 'a', 'quoter' : '>', 'raw' : '> a' } ],
               [ { 'text' : 'b', 'quoter' : '=>', 'raw' : '=> b' } ],
               [ { 'text' : 'c', 'quoter' : '>', 'raw' : '> c' } ]
            ]
        x = self._massage(x)
        self.assertEqual( extract(g), x )

