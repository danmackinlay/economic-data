from __future__ import division
#NB rpy2 only compiles for 64 bit python out of the box.
# from rpy2.robjects.packages import importr
from sqlalchemy import create_engine, Table, Column, MetaData, BigInteger, SmallInteger, Integer, String, Float, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
SITC rev 4 trade codes are documented at URLs like this:
http://unstats.un.org/unsd/cr/registry/regcs.asp?Cl=14&Lg=1&Co=723.21
A complete list of codes is in S4BH.xls, and an unparseable plaintext in SeriesM_34rev4E.pdf but the UN web pages will need to be scraped for the whole goss.
http://unstats.un.org/unsd/cr/registry/regcs.asp?Cl=28&Lg=1&Co=121
"""


#this works, but is astonishingly slow. Too slow to be useable.
# foreign = importr('foreign')
# wtf=foreign.read_dta("/Users/dan/Desktop/researchtmp/un/wtf62.dta")
# col_names = wtf.names
# for row in wtf.iter_row():
#     print dict(zip(col_names, [e[0] for e in row]))
    
from sqlalchemy import create_engine, Table, Column, MetaData, BigInteger, SmallInteger, Integer, String, Float, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sqlite://<nohostname>/<path>
# where <path> is relative:
engine = create_engine('sqlite:///tradeflow.db')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# example record
# {'exporter': 'Zambia', 'value': 216, 'ecode': '168940', 'importer': 'World', 'icode': '100000', 'dot': NA_integer_, 'year': 1962, 'sitc4': '7131', 'unit': '', 'quantity': NA_integer_}
# 
# class Flow(Base):
#     __tablename__='wtf'
#     id = Column(Integer, Sequence('ipc_id_seq'), primary_key=True, autoincrement=True)
#     appyear = Column(Integer)
#     cat = Column(SmallInteger)
#     gyear = Column(SmallInteger)
#     icl = Column(String(18), index=True)
#     icl_class = Column(String(4))
#     icl_maingroup = Column(Float)
#     iclnum = Column(SmallInteger)
#     nclass = Column(Integer)
#     numipc = Column(SmallInteger)
#     patent = Column(BigInteger, index=True)
#     pdpass = Column(BigInteger)
#     subcat = Column(SmallInteger)
#     subclass = Column(Float)
#     uspto_assignee = Column(BigInteger, index=True)
