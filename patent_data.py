from __future__ import division
import sys
from statsmodels.iolib.foreign import StataReader
from sqlalchemy import create_engine, Table, Column, MetaData, BigInteger, SmallInteger, Integer, String, Float, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from patent_local_settings import DB_URL

# sqlite://<nohostname>/<path>
# where <path> is relative:
engine = create_engine(DB_URL)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

# http://docs.sqlalchemy.org/en/rel_0_7/core/schema.html#metadata-constraints
# http://docs.sqlalchemy.org/en/rel_0_7/orm/relationships.html
# http://docs.sqlalchemy.org/en/rel_0_7/orm/tutorial.html
# http://docs.sqlalchemy.org/en/rel_0_7/core/tutorial.html
# http://docs.sqlalchemy.org/en/rel_0_7/orm/extensions/declarative.html

#This file has one record for each IPC class for each patent. The data description is:
"""
-------------------------------------------------------------------------------
              storage  display     value
variable name   type   format      label      variable label
-------------------------------------------------------------------------------
appyear         int    %8.0g                  Year patent applied for
cat             byte   %8.0g                  HJT tech category (1-6) for CCL
gyear           int    %8.0g                  Year patent granted
icl             str18  %18s                   clas/international
                                                classification
icl_class       str4   %9s                    Main 4-char IPC
icl_maingroup   float  %9.0g                  Main group within 4char IPC
iclnum          byte   %8.0g                  clas/icl seq. number (imc)
nclass          int    %9.0g                  US 3-digit current
                                                classification (CCL)
numipc          byte   %9.0g                  Number of international patent
                                                classes
patent          long   %12.0g                 Patent number (7-digit)
pdpass          long   %12.0g                 Unique assignee number
subcat          byte   %8.0g                  HJT tech subcategory (11-69)
                                                for CCL
subclass        float  %9.0g                  Subclass for US current class
                                                (CCL)
uspto_assignee  long   %12.0g                 Original assignee number
-------------------------------------------------------------------------------
Sorted by:  patent  pdpass  iclnum
"""

class Ipc(Base):
    __tablename__='ipc'
    id = Column(Integer, Sequence('ipc_id_seq'), primary_key=True, autoincrement=True)
    appyear = Column(Integer)
    cat = Column(SmallInteger)
    gyear = Column(SmallInteger)
    icl = Column(String(18), index=True)
    icl_class = Column(String(4))
    icl_maingroup = Column(Float)
    iclnum = Column(SmallInteger)
    nclass = Column(Integer)
    numipc = Column(SmallInteger)
    patent = Column(BigInteger, index=True)
    pdpass = Column(BigInteger)
    subcat = Column(SmallInteger)
    subclass = Column(Float)
    uspto_assignee = Column(BigInteger, index=True)

#This file has one record for each assignment of each utility patent. Patents that are assigned to more than one party have multiple records. This file lists only the first technology class.
"""
-------------------------------------------------------------------------------
              storage  display     value
variable name   type   format      label      variable label
-------------------------------------------------------------------------------
allcites        int    %9.0g                  Cites 1976-2006 (not adj for
                                                truncation)
appyear         int    %8.0g                  Year patent applied for
asscode         byte   %8.0g                  Original assignee code (1-7)
assgnum         byte   %8.0g                  assg/assignee seq. number (imc)
cat             byte   %8.0g                  HJT tech category (1-6) for CCL
cat_ocl         byte   %8.0g                  HJT tech category (1-6) for OCL
cclass          str11  %11s                   Primary current US
                                                class/subclass (Alpha)
country         str2   %9s                    assg/country
ddate           float  %d                     patn/disclaimer date
gday            byte   %8.0g                  Day patent granted
gmonth          byte   %8.0g                  Month patent granted
gyear           int    %8.0g                  Year patent granted
hjtwt           float  %9.0g                  Citation truncation weight as
                                                of 2006
icl             str18  %18s                   clas/international
                                                classification
icl_class       str4   %9s                    Main 4-char IPC
icl_maingroup   float  %9.0g                  Main group within 4char IPC
iclnum          byte   %8.0g                  clas/icl seq. number (imc)
nclaims         int    %9.0g                  patn/number of claims
nclass          int    %9.0g                  US 3-digit current
                                                classification (CCL)
nclass_ocl      int    %9.0g                  US 3-digit original
                                                classification (OCL)
patent          long   %12.0g                 Patent number (7-digit)
pdpass          long   %12.0g                 Unique assignee number
state           str2   %2s                    assg/state
status          str1   %1s                    auth/status: m missing, w
                                                withdrawn
subcat          byte   %8.0g                  HJT tech subcategory (11-69)
                                                for CCL
subcat_ocl      byte   %8.0g                  HJT tech subcategory (11-69)
                                                for OCL
subclass        float  %9.0g                  Subclass for US current class
                                                (CCL)
subclass1       str9   %9s                    Subclass for US current class
                                                (CCL) - Alpha
subclass1_ocl   str9   %9s                    Subclass for US original class
                                                (OCL) - Alpha
subclass_ocl    float  %9.0g                  Subclass for US original class
                                                (OCL)
term_extension  int    %9.0g                  patn/extension of patent term
                                                in days under 35 usc 154(b)
uspto_assignee  long   %12.0g                 Original assignee number
-------------------------------------------------------------------------------
Sorted by:  patent
"""

class Assignment(Base):
    __tablename__='assg'
    id = Column(Integer, Sequence('assg_id_seq'), primary_key=True, autoincrement=True)
    allcites = Column(Integer)
    appyear = Column(Integer)
    asscode = Column(SmallInteger)
    assgnum = Column(Integer)
    cat = Column(SmallInteger)
    cat_ocl = Column(SmallInteger)
    cclass = Column(String(11))
    country = Column(String(2))
    ddate = Column(Float)
    gday = Column(SmallInteger)
    gmonth = Column(SmallInteger)
    gyear = Column(SmallInteger)
    hjtwt = Column(Float)
    icl = Column(String(18), index=True)
    icl_class = Column(String(4))
    icl_maingroup = Column(Float)
    iclnum = Column(SmallInteger)
    nclaims = Column(Integer)
    nclass = Column(Integer)
    nclass_ocl = Column(Integer)
    patent = Column(BigInteger, index=True)
    pdpass = Column(BigInteger,index=True)
    state = Column(String(2))
    status = Column(String(1))
    subcat = Column(SmallInteger)
    subcat_ocl = Column(SmallInteger)
    subclass = Column(Float)
    subclass1 = Column(String(9))
    subclass1_ocl = Column(String(9))
    subclass_ocl = Column(Float)
    term_extension = Column(Integer)
    uspto_assignee = Column(BigInteger, index=True)
    
"""
Patent classification:

The USPTO changes its classification system from time to time to accommodate 
the growth in new technologies, adding classes, and occasionally deleting old 
classes if they become too full (creating a whole new set of classes to replace 
them).

The variables designated "OCL" are based on the original classification at the 
time the patent was examined and issued (the field of search shown on the USPTO 
website). Therefore the classificaiton system used will vary across the patents 
in the file according to their vintage.

The variables designated "CCL" are based on the USPTO classification system as 
of 2008. This means that all the patents on this file will have a consistent 
classification applied if you use the ccl variables. The category and 
subcategory assignments are listed in this spreadsheet. Note that the 
categories do not fully correspond to early technology classes (such as 2006 or 
nclass) because, of course, the USPTO continually revises the technology 
classes.

IPC codes are assigned via a concordance from the USPTO codes. The USPC to IPC 
Concordance is based on the International Patent Classification Eighth Edition 
(please see note at the bottom of this page ).
"""

Base.metadata.create_all()

def main():
    global ipc_data, assg_data
    # ipc_data_handle = open('/Users/dan/Dropbox/trade_data/nber_Data/patents/pat76_06_ipc.dta')
    ipc_data_handle = open('/Users/dan/Desktop/researchtmp/pat76_06_ipc.dta')
    ipc_data = StataReader(ipc_data_handle)
    n_recs = len(ipc_data)

    for i, stata_rec in enumerate(ipc_data.dataset(as_dict=True)):
        db_rec = Ipc(**stata_rec)
        session.add(db_rec)
        if (i % 10000) == 0:
            session.commit()
            print "ipc: %f%%" % (100.0*i/n_recs)

    # assg_data_handle = open('/Users/dan/Dropbox/trade_data/nber_Data/patents/pat76_06_assg.dta')
    assg_data_handle = open('/Users/dan/Desktop/researchtmp/pat76_06_assg.dta')
    assg_data = StataReader(assg_data_handle)
    n_recs = len(assg_data)

    for i, stata_rec in enumerate(assg_data.dataset(as_dict=True)):
        db_rec = Assignment(**stata_rec)
        session.add(db_rec)
        if (i % 10000) == 0:
            session.commit()
            print "assg: %f%%" % (100.0*i/n_recs)

