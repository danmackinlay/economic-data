"""
SITC rev 4 trade codes are documented at URLs like this:
http://unstats.un.org/unsd/cr/registry/regcs.asp?Cl=14&Lg=1&Co=723.21
A complete list of codes is in S4BH.xls, and an unparseable plaintext in SeriesM_34rev4E.pdf but the UN web pages will need to be scraped for the whole goss.
http://unstats.un.org/unsd/cr/registry/regcs.asp?Cl=28&Lg=1&Co=121
"""

#NB rpy2 only compiles for 64 bit python out of the box.
from rpy2.robjects.packages import importr

#this works, but is astonishingly slow. Too slow to be useable.
foreign = importr('foreign')
wtf=foreign.read_dta("/Users/dan/Desktop/researchtmp/un/wtf62.dta")
col_names = wtf.names
for row in wtf.iter_row():
    print dict(zip(col_names, [e[0] for e in row]))