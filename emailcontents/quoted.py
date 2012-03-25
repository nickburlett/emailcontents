"""
Python port of perl's Text::Quoted. 

Example
=======

> from emailcontents.quoted import extract
> structure = extract( text );

Description
===========

`extract` examines the structure of some text which may contain multiple
different levels of quoting, and turns the text into a nested data structure. 

The structure is an array containing dictionary for each paragraph belonging to
the same author (quote depth). Each level of quoting recursively adds another
list reference. So for instance, this:

\"\"\"\\
> foo
> # Bar
> baz

quux
\"\"\"

turns into:

[
  [
    { text : 'foo', quoter : '>', raw : '> foo' },
    [ 
        { text : 'Bar', quoter : '> #', raw : '> # Bar' } 
    ],
    { text : 'baz', quoter : '>', raw : '> baz' }
  ],

  { empty : True },
  { text : 'quux', quoter : '', raw : 'quux' }
];

This also tells you about what's in the dictionary: `'raw'` is the
paragraph of text as it appeared in the original input; `'text'` is what
it looked like when we stripped off the quotation characters, and `'quoter'`
is the quotation string.


About the original Text::Quoted
===============================

Most of the heavy lifting is done by a modified version of Damian Conway's
Text::Autoformat.

COPYRIGHT
---------

Copyright (C) 2002-2003 Kasei Limited
Copyright (C) 2003-2004 Simon Cozens
Copyright (C) 2004 Best Practical Solutions, LLC

This software is distributed WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

The Text::Quoted library is free software; you can redistribute it and/or
modify it under the same terms as Perl itself.

About this port
===============

This port follows the original Text::Quoted as closesly as possible
while attempting to make it somewhat pythonic.

This software is distributed WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

The emailcontents.quoted library is free software; you can redistribute it
and/or modify it under the terms of the Artistic License.
"""

import re


def extract(text):
    """Extract the quoted paragraphs from an email text"""
    ret = organize( "", classify( text ) );
    if len(ret) == 1:
        return ret[0]
    else:
        return ret



def organize( top_level, todo ):
    """
    Recursively form a data structure which reflects the quoting
    structure of the list.
    """
    ret = []


    while len(todo):
        line = todo.pop(0)
        q = line.get('quoter', '')
        if q == top_level:
            ## Just append lines at "my" level.
            if 'quoter' in line or 'empty' in line:
                ret.append(line)
        elif q.startswith(top_level) and len(q) > len(top_level):
            ## Find all the lines at a quoting level "below" me.
            newquoter = find_below( top_level, line, *todo )
            next = [line]
            while len(todo) and todo[0].get('quoter') and todo[0]['quoter'].startswith(newquoter):
                next.append( todo.pop(0) )

            ## Find the 
            ## And pass them on to organize()!
            ret.append( organize( newquoter, next ) )

    return ret

## Given, say:
##   X
##   > > hello
##   > foo bar
##   Stuff
##
## After "X", we're moving to another level of quoting - but which one?
## Naively, you'd pick out the prefix of the next line, "> >", but this
## is incorrect - "> >" is actually a "sub-quote" of ">". This routine
## works out which is the next level below us.

def find_below( top_level, *stuff ):
    """
    Find the prefices, shortest first.
    And return the first one which is "below" where we are right
    now but is a proper subset of the next line. 
    """
    vals = [ (len(x['quoter']), x['quoter']) for x in stuff if x['quoter'].startswith(top_level) and len(x['quoter']) > len(top_level) and stuff[0]['quoter'].startswith(x['quoter']) ]
    return sorted(vals)[0][1]


## Everything below this point is essentially Text::Autoformat.

## BITS OF A TEXT LINE

_quotechar = r'[!#%=|:]'
_quotechar_re = re.compile(_quotechar)
_separator = r'[-_]{2,}|[=#*]{3,}|[+~]{4,}'
_separator_re = re.compile(_separator)
_quotechunk = r'(?!(?:'+_separator+r") *\Z)(?:"+_quotechar+r"(?!\w)|\w*>+)"
_quotechunk_re = re.compile( _quotechunk )
_quoter = _quotechunk + r'(?:[ \t]*' + _quotechunk + r')*'
_quoter_re = re.compile( _quoter )


_quotersplit = r"\A *((?:" + _quoter + ")?) *(.*?)\s*\Z"
_quotersplit_re = re.compile(_quotersplit)

_separatorx = r"\A *(" + _separator + r") *\Z"
_separator_re = re.compile( _separatorx )

def _matchgroups(re, txt):
    matches = re.match(txt)
    if matches:
        return matches.groups()
    return None


def classify(text):
    ## If the user passes in a null string, we really want to end up with _something_
    if text == "" or not isinstance(text, basestring):
        return [{ "raw": "", "text": "", "quoter": "", "separator":False, "empty": True }]


    ## DETABIFY
    lines = ( ln.expandtabs() for ln in text.splitlines() )


    ## PARSE EACH LINE
    newlines = []
    for ln in lines:
        line = { 'raw': ln }
        line['quoter'], line['text'] = _matchgroups(_quotersplit_re, ln ) or ("", "")
        line['empty'] =  line['text'].strip() == ""
        line['separator'] = bool(_separator_re.match( line['text'] ))
        newlines.append( line )
    lines = newlines

    ## SUBDIVIDE DOCUMENT INTO COHERENT SUBSECTIONS

    chunks = [ [ lines.pop(0) ] ]
    for line in lines:
        if (  line['separator'] 
           or line['quoter'] != chunks[-1][-1]['quoter'] 
           or line['empty']
           or chunks[-1][-1]['empty'] ):
            chunks.append( [ line ] ) 
        else:
            chunks[-1].append( line )

    ## REDIVIDE INTO PARAGRAPHS

    paras = []
    for chunk in chunks:
        first = True
        firstfrom = None
        for line in chunk:
            if (  first
               or line['quoter'] != paras[-1]['quoter']
               or paras[-1]['separator'] ):
                paras.append( line )
                first = False
                firstfrom = len( line.get('raw', '') ) - len( line.get('text', '' ) )
            else:
                extraspace = len( line['raw'] ) - len( line['text'] ) - firstfrom
                paras[-1]['text'] += "\n" + " "*extraspace + line['text']
                paras[-1]['raw'] += "\n" + line['raw']

    return paras
