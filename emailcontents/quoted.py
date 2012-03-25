import re

#package Text::Quoted;
#our $VERSION = "2.06";
#use 5.006;
#use strict;
#use warnings;

#require Exporter;

#our @ISA    = qw(Exporter);
#our @EXPORT = qw(extract);

#use Text::Autoformat();    # Provides the Hang package, heh, heh.

#=head1 NAME

#Text::Quoted - Extract the structure of a quoted mail message

#=head1 SYNOPSIS

    #use Text::Quoted;
    #my $structure = extract($text);

#=head1 DESCRIPTION

#C<Text::Quoted> examines the structure of some text which may contain
#multiple different levels of quoting, and turns the text into a nested
#data structure. 

#The structure is an array reference containing hash references for each
#paragraph belonging to the same author. Each level of quoting recursively
#adds another list reference. So for instance, this:

    #> foo
    #> # Bar
    #> baz

    #quux

#turns into:

    #[
      #[
        #{ text => 'foo', quoter => '>', raw => '> foo' },
        #[ 
            #{ text => 'Bar', quoter => '> #', raw => '> # Bar' } 
        #],
        #{ text => 'baz', quoter => '>', raw => '> baz' }
      #],

      #{ empty => 1 },
      #{ text => 'quux', quoter => '', raw => 'quux' }
    #];

#This also tells you about what's in the hash references: C<raw> is the
#paragraph of text as it appeared in the original input; C<text> is what
#it looked like when we stripped off the quotation characters, and C<quoter>
#is the quotation string.

#=cut

#sub extract {
def extract(text):
    #return organize( "", classify( @_ ) );
    ret = organize( "", classify( text ) );
    if len(ret) == 1:
        return ret[0]
    else:
        return ret
#}

#=head1 CREDITS

#Most of the heavy lifting is done by a modified version of Damian Conway's
#C<Text::Autoformat>.

#=head1 COPYRIGHT

#Copyright (C) 2002-2003 Kasei Limited
#Copyright (C) 2003-2004 Simon Cozens
#Copyright (C) 2004 Best Practical Solutions, LLC

#This software is distributed WITHOUT ANY WARRANTY; without even the implied
#warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

#This library is free software; you can redistribute it and/or modify
#it under the same terms as Perl itself. 

#=cut

def organize( top_level, todo ):
#sub organize {
    #my $top_level = shift;
    #my @todo      = @_;
    #$top_level = '' unless defined $top_level;


    #my @ret;
    ret = []


    ## Recursively form a data structure which reflects the quoting
    ## structure of the list.
    #while (my $line = shift @todo) {
    while len(todo):
        line = todo.pop(0)
        #my $q = defined $line->{quoter}? $line->{quoter}: '';
        q = line.get('quoter', '')
        #if ( $q eq $top_level ) {
        if q == top_level:
            ## Just append lines at "my" level.
            #push @ret, $line
              #if exists $line->{quoter}
              #or exists $line->{empty};
            if 'quoter' in line or 'empty' in line:
                ret.append(line)
        #}
        #elsif ( $q =~ /^\Q$top_level\E./ ) {
        elif q.startswith(top_level) and len(q) > len(top_level):
            ## Find all the lines at a quoting level "below" me.
            #my $newquoter = find_below( $top_level, $line, @todo );
            newquoter = find_below( top_level, line, *todo )
            #my @next = $line;
            next = [line]
            #push @next, shift @todo while defined $todo[0]->{quoter}
              #and $todo[0]->{quoter} =~ /^\Q$newquoter/;
            while len(todo) and todo[0].get('quoter') and todo[0]['quoter'].startswith(newquoter):
                next.append( todo.pop(0) )

            ## Find the 
            ## And pass them on to organize()!
            ##print "Trying to organise the following lines over $newquoter:\n";
            ##print $_->{raw}."\n" for @next;
            ##print "!-!-!-\n";
            #push @ret, organize( $newquoter, @next );
            ret.append( organize( newquoter, next ) )
        #} #  else { die "bugger! I had $top_level, but now I have $line->{raw}\n"; }
    #}
    #return \@ret;
    return ret
#}

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

#sub find_below {
def find_below( top_level, *stuff ):
    #my ( $top_level, @stuff ) = @_;

    ## Find the prefices, shortest first.
    ## And return the first one which is "below" where we are right
    ## now but is a proper subset of the next line. 
    #return (
        #sort { length $a <=> length $b }
        #grep $_ && /^\Q$top_level\E./ && $stuff[0]->{quoter} =~ /^\Q$_\E/,
        #map $_->{quoter},
        #@stuff 
    #)[0];
    vals = [ (len(x['quoter']), x['quoter']) for x in stuff if x['quoter'].startswith(top_level) and len(x['quoter']) > len(top_level) and stuff[0]['quoter'].startswith(x['quoter']) ]
    return sorted(vals)[0][1]

#}

## Everything below this point is essentially Text::Autoformat.

## BITS OF A TEXT LINE

#my $quotechar  = qr/[!#%=|:]/;
_quotechar = r'[!#%=|:]'
_quotechar_re = re.compile(_quotechar)
#my $separator  = qr/[-_]{2,} | [=#*]{3,} | [+~]{4,}/x;
_separator = r'[-_]{2,}|[=#*]{3,}|[+~]{4,}'
_separator_re = re.compile(_separator)
#my $quotechunk = qr/(?!$separator *\z)(?:$quotechar(?!\w)|\w*>+)/;
_quotechunk = r'(?!(?:'+_separator+r") *\Z)(?:"+_quotechar+r"(?!\w)|\w*>+)"
_quotechunk_re = re.compile( _quotechunk )
#my $quoter     = qr/$quotechunk(?:[ \t]*$quotechunk)*/;
_quoter = _quotechunk + r'(?:[ \t]*' + _quotechunk + r')*'
_quoter_re = re.compile( _quoter )

#sub defn($) { return $_[0] if (defined $_[0]); return "" }
def defn(x):
    if len(x):
        return x[0]
    else:
        return ""

_quotersplit = r"\A *((?:" + _quoter + ")?) *(.*?)\s*\Z"
_quotersplit_re = re.compile(_quotersplit)

_separatorx = r"\A *(" + _separator + r") *\Z"
_separator_re = re.compile( _separatorx )

def _matchgroups(re, txt):
    matches = re.match(txt)
    if matches:
        return matches.groups()
    return None


#sub classify {
def classify(text):
    #my $text = shift;
    #return { raw => undef, text => undef, quoter => undef }
        #unless defined $text && length $text;
    ## If the user passes in a null string, we really want to end up with _something_
    if text == "" or not isinstance(text, basestring):
        return [{ "raw": "", "text": "", "quoter": "", "separator":False, "empty": True }]


    ## DETABIFY
    #my @lines = expand_tabs( split /\n/, $text );
    lines = ( ln.expandtabs() for ln in text.splitlines() )


    ## PARSE EACH LINE
    newlines = []
    #foreach (splice @lines) {
    for ln in lines:
        #my %line = ( raw => $_ );
        line = { 'raw': ln }
        #@line{'quoter', 'text'} = (/\A *($quoter?) *(.*?)\s*\Z/o);
        line['quoter'], line['text'] = _matchgroups(_quotersplit_re, ln ) or ("", "")
        #$line{hang}      = Hang->new( $line{'text'} );
        #line['hang'] = Hang( line['text'] )
        #$line{empty}     = 1 if $line{hang}->empty() && $line{'text'} !~ /\S/;
        line['empty'] =  line['text'].strip() == ""
        #$line{separator} = 1 if $line{text} =~ /\A *$separator *\Z/o;
        line['separator'] = bool(_separator_re.match( line['text'] ))
        #push @lines, \%line;
        newlines.append( line )
    #}
    lines = newlines

    ## SUBDIVIDE DOCUMENT INTO COHERENT SUBSECTIONS

    #my @chunks;
    #push @chunks, [ shift @lines ];
    chunks = [ [ lines.pop(0) ] ]
    #foreach my $line (@lines) {
    for line in lines:
        #if ( $line->{separator}
            #|| $line->{quoter} ne $chunks[-1][-1]->{quoter}
            #|| $line->{empty}
            #|| $chunks[-1][-1]->{empty} )
        if (  line['separator'] 
           or line['quoter'] != chunks[-1][-1]['quoter'] 
           or line['empty']
           or chunks[-1][-1]['empty'] ):
        #{
            #push @chunks, [$line];
            chunks.append( [ line ] ) 
        #}
        #else {
        else:
            #push @{ $chunks[-1] }, $line;
            chunks[-1].append( line )
        #}
    #}

    ## REDIVIDE INTO PARAGRAPHS

    #my @paras;
    paras = []
    #foreach my $chunk (@chunks) {
    for chunk in chunks:
        #my $first = 1;
        first = True
        #my $firstfrom;
        firstfrom = None
        #foreach my $line ( @{$chunk} ) {
        for line in chunk:
            #if ( $first
                #|| $line->{quoter} ne $paras[-1]->{quoter}
                #|| $paras[-1]->{separator} )
            if (  first
               or line['quoter'] != paras[-1]['quoter']
               or paras[-1]['separator'] ):
            #{
                #push @paras, $line;
                paras.append( line )
                #$first     = 0;
                first = False
		## We get warnings from undefined raw and text values if we don't supply alternates
                #$firstfrom = length( $line->{raw} ||'' ) - length( $line->{text} || '');
                firstfrom = len( line.get('raw', '') ) - len( line.get('text', '' ) )
            #}
            #else {
            else:
                #my $extraspace =
                  #length( $line->{raw} ) - length( $line->{text} ) - $firstfrom;
                extraspace = len( line['raw'] ) - len( line['text'] ) - firstfrom
                #$paras[-1]->{text} .= "\n" . q{ } x $extraspace . $line->{text};
                paras[-1]['text'] += "\n" + " "*extraspace + line['text']
                #$paras[-1]->{raw} .= "\n" . $line->{raw};
                paras[-1]['raw'] += "\n" + line['raw']
            #}
        #}
    #}

    ## Reapply hangs
    #for (grep $_->{'hang'}, @paras) {
    #for elm in paras:
        #if not elm.has_attr('hang'):
            #continue
        #next unless my $str = (delete $_->{hang})->stringify;
        #mystr = elm['hang'].stringify()
        #del elm['hang']
        #$_->{text} = $str . " " . $_->{text};
        #elm['text'] = mystr + " " + elm['text']
    #}
    #return @paras;
    return paras
#}
