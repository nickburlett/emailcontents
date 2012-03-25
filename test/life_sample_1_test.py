from base import BaseTest
from emailcontents.quoted import extract

a = """\
>>>>> "dc" == darren chamberlain writes:

>> If I don't do "use Template;" in my startup script, each child will
>> get the pleasure of loading and compiling it all when the first script
>> that uses Template gets executed.

dc> Unless one of the other modules that you use in your startup script
dc> happens to use Template, in which case you'll be OK.

Well, that's still "use Template;" as far as I'm concerned.

I was really just being pedantic...  but think of a hosting situation
where the startup is pretty bare, and some Registry program uses the
template.

I personally don't think the preload should be called automagically,
even if it does the right thing most of the time.

_______________________________________________
templates mailing list
templates@template-toolkit.org
http://www.template-toolkit.org/mailman/listinfo/templates
"""

expected =  [
          [
            [
              {
                'quoter' : '>>>>>',
                'text' : '"dc" == darren chamberlain writes:',
                'raw' : '>>>>> "dc" == darren chamberlain writes:',
              }
            ]
          ],
          {
            'quoter' : '',
            'text' : '',
            'raw' : '',
            'empty' : '1'
          },
          [
            {
              'quoter' : '>>',
              'text' : '''If I don\'t do "use Template;" in my startup script, each child will
get the pleasure of loading and compiling it all when the first script
that uses Template gets executed.''',
              'raw' : '''>> If I don\'t do "use Template;" in my startup script, each child will
>> get the pleasure of loading and compiling it all when the first script
>> that uses Template gets executed.''',
            }
          ],
          {
            'quoter' : '',
            'text' : '',
            'raw' : '',
            'empty' : '1'
          },
          [
            {
              'quoter' : 'dc>',
              'text' : '''Unless one of the other modules that you use in your startup script
happens to use Template, in which case you\'ll be OK.''',
              'raw' : '''dc> Unless one of the other modules that you use in your startup script
dc> happens to use Template, in which case you\'ll be OK.''',
            }
          ],
          {
            'quoter' : '',
            'text' : '',
            'raw' : '',
            'empty' : '1'
          },
          {
            'quoter' : '',
            'text' : 'Well, that\'s still "use Template;" as far as I\'m concerned.',
            'raw' : 'Well, that\'s still "use Template;" as far as I\'m concerned.',
          },
          {
            'quoter' : '',
            'text' : '',
            'raw' : '',
            'empty' : '1'
          },
          {
            'quoter' : '',
            'text' : '''I was really just being pedantic...  but think of a hosting situation
where the startup is pretty bare, and some Registry program uses the
template.''',
            'raw' : '''I was really just being pedantic...  but think of a hosting situation
where the startup is pretty bare, and some Registry program uses the
template.''',
          },
          {
            'quoter' : '',
            'text' : '',
            'raw' : '',
            'empty' : '1'
          },
          {
            'quoter' : '',
            'text' : '''I personally don\'t think the preload should be called automagically,
even if it does the right thing most of the time.''',
            'raw' : '''I personally don\'t think the preload should be called automagically,
even if it does the right thing most of the time.''',
          },
          {
            'quoter' : '',
            'text' : '',
            'raw' : '',
            'empty' : '1'
          },
          {
            'separator' : '1',
            'quoter' : '',
            'text' : '_______________________________________________',
            'raw' : '_______________________________________________',
          },
          {
            'quoter' : '',
            'text' : '''templates mailing list
templates@template-toolkit.org
http://www.template-toolkit.org/mailman/listinfo/templates''',
            'raw' : '''templates mailing list
templates@template-toolkit.org
http://www.template-toolkit.org/mailman/listinfo/templates''',
          }
        ]

b = """\
From: "Brian Christopher Robinson" <brian.c.robinson@trw.com>
zxc
> > An
> > alternative solution is to not have those phone calls at work,
> > faciliitated by worked very hard for a reasonably workday, then
> > leaving... thus having time to deal with personal issues when not at
> > work.
iabc
> Unfortunately, personal issues can't be conveniently shoved aside
eight
> hours a day.  People with kids especially have to deal with issues
> realted to picking them up and dropping them off at various times, as
x
"""

expected_b = [
          {
            'quoter' : '',
            'text' : '''From: "Brian Christopher Robinson" <brian.c.robinson@trw.com>
zxc''',
            'raw' : '''From: "Brian Christopher Robinson" <brian.c.robinson@trw.com>
zxc''',
          },
          [
            [
              {
                'quoter' : '> >',
                'text' : '''An
alternative solution is to not have those phone calls at work,
faciliitated by worked very hard for a reasonably workday, then
leaving... thus having time to deal with personal issues when not at
work.''',
                'raw' : '''> > An
> > alternative solution is to not have those phone calls at work,
> > faciliitated by worked very hard for a reasonably workday, then
> > leaving... thus having time to deal with personal issues when not at
> > work.''',
              }
            ]
          ],
          {
            'quoter' : '',
            'text' : 'iabc',
            'raw' : 'iabc',
          },
          [
            {
              'quoter' : '>',
              'text' : 'Unfortunately, personal issues can\'t be conveniently shoved aside',
              'raw' : '> Unfortunately, personal issues can\'t be conveniently shoved aside',
            }
          ],
          {
            'quoter' : '',
            'text' : 'eight',
            'raw' : 'eight',
          },
          [
            {
              'quoter' : '>',
              'text' : '''hours a day.  People with kids especially have to deal with issues
realted to picking them up and dropping them off at various times, as''',
              'raw' : '''> hours a day.  People with kids especially have to deal with issues
> realted to picking them up and dropping them off at various times, as''',
            }
          ],
          {
            'quoter' : '',
            'text' : 'x',
            'raw' : 'x',
          }
        ]

ntk = """\
 _   _ _____ _  __ <*the* weekly high-tech sarcastic update for the uk>
| \ | |_   _| |/ / _ __   __2002-07-26_ o join! mail an empty message to
|  \| | | | | ' / | '_ \ / _ \ \ /\ / / o ntknow-subscribe@lists.ntk.net
| |\  | | | | . \ | | | | (_) \ v  v /  o website (+ archive) lives at:
|_| \_| |_| |_|\_\|_| |_|\___/ \_/\_/   o     http://www.ntk.net/ 
"""

class LifeSampleTest(BaseTest):
    def test(self):
        "Real world test"
        x = self._massage(expected)
        self.assertEqual( extract(a), x )

    def test_b(self):
        "Real world test b"
        x = self._massage(expected_b)
        self.assertEqual( extract(b), x )

    def test_ntk(self):
        "Wow... don't segfault"
        extract(ntk)
