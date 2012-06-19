from statsmodels.iolib.foreign import StataReader
from sqlalchemy import create_engine, Table, Column, MetaData, BigInteger, SmallInteger, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# sqlite://<nohostname>/<path>
# where <path> is relative:
Base = declarative_base(bind = create_engine('sqlite:///patent.db'))

# http://docs.sqlalchemy.org/en/rel_0_7/core/schema.html#metadata-constraints
# http://docs.sqlalchemy.org/en/rel_0_7/orm/relationships.html
# http://docs.sqlalchemy.org/en/rel_0_7/orm/tutorial.html
# http://docs.sqlalchemy.org/en/rel_0_7/core/tutorial.html
# http://docs.sqlalchemy.org/en/rel_0_7/orm/extensions/declarative.html

def type_for_dta(typ):
    type_for_dta = {
        'h': Integer,
        'b': SmallInteger,
        'l': BigInteger,
        'f': Float,
        'd': Float
    }
    if typ in type_for_dta: return type_for_dta[typ]
    #else it is an integer, denoting string of a given length
    return String(typ)

def columns_for_dta(dta, primary):
    for v in dta.variables():
        print v.name, v.type, v.label, type_for_dta(v.type)
        yield v.name, Column(v.name, type_for_dta(v.type), primary_key = True if v.name in primary else None)
    
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
# ipc_data_handle = open('/Users/dan/Dropbox/trade_data/nber_Data/patents/pat76_06_ipc.dta')
ipc_data_handle = open('/Users/dan/Desktop/researchtmp/pat76_06_ipc.dta')
ipc_data = StataReader(ipc_data_handle)

class Ipc(Base):
    __tablename__='ipc'
    # appyear = Column(Integer)
    # cat = Column(SmallInteger)
    # gyear = Column(SmallInteger)
    # icl = Column(String(18), primary_key=True)
    # icl_class = Column(String(4))
    # icl_maingroup = Column(Float)
    # iclnum = Column(SmallInteger)
    # nclass = Column(Integer)
    # numipc = Column(SmallInteger)
    # patent = Column(BigInteger)
    # pdpass = Column(BigInteger)
    # subcat = Column(SmallInteger)
    # subclass = Column(Float)
    # uspto_assignee = Column(BigInteger)

for name, col in columns_for_dta(ipc_data, primary= ['icl']):
    setattr(Ipc, name, col)

    
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
# assg_data_handle = open('/Users/dan/Dropbox/trade_data/nber_Data/patents/pat76_06_assg.dta')
# assg_data_handle = open('/Users/dan/Desktop/researchtmp/pat76_06_assg.dta')
# assg_data = StataReader(assg_data_handle)
# 
metadata.create_all()