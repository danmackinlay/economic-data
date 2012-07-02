"""
Here is a list of Australian Companies by category:
http://www.asx.com.au/asx/research/companyInfo.do

Here is the format of Yahoo Finance downloads by category:
http://ichart.finance.yahoo.com/table.csv?d=6&e=1&f=2012&g=d&a=7&b=19&c=2003&ignore=.csv&s=ASX.AX

TODO:

* Think about foriegn exchanges' data, not just ASX
* what to do with missing data (so far, only companies that did not yet exist or folded)
* gzip data to save space
* return just a 2-column data set.
* how to represent dates? Ints, preferably.
"""

import requests
import csv
import os.path
import gzip
from settings import EQUITY_CACHE_DIR

YAHOO_URL_TEMPLATE = "http://ichart.finance.yahoo.com/table.csv?d=6&e=1&f=2012&g=d&a=1&b=1&c=2003&ignore=.csv&s=%s.AX"

FAVOURITE_FIRMS = \
{'1010': {
          'ORG': u'ORIGIN ENERGY',
          'RRS': u'RANGE RESOURCES LTD',
          'RUM': u'RUM JUNGLE RES',},
 '1510': {'AAI': u'ALCOA INC.',
          'BHP': u'BHP BILLITON LIMITED',
          'CYU': u'CHINALCO YUNNAN',
          'EAU': u'ELDORADO GOLD CORP',
          'FMG': u'FORTESCUE METALS GRP',
          'GDA': u'GONDWANA RESOURCES',
          'NCM': u'NEWCREST MINING',
          'ORD': u'ORD RIVER RESOURCES',
          'ORI': u'ORICA LIMITED',
          'OST': u'ONESTEEL LIMITED',
          'ZRI': u'RIO TINTO PLC',},
 '2010': {'CLO': u'CLOUGH LIMITED',
          'CSR': u'CSR LIMITED',},
 '2020': {'BXB': u'BRAMBLES LIMITED',
          'TSE': u'TRANSFIELD SERVICES',
          'ZBI': u'BRAMBLES IND. PLC'},
 '2030': {'AIZ': u'AIR NEW ZEALAND',
          'CLX': u'CTI LOGISTICS',
          'QAN': u'QANTAS AIRWAYS',
          'QRN': u'QR NATIONAL LIMITED',
          'SYD': u'SYD AIRPORT',},
 '2510': {'ION': u'ION LIMITED',
          'OEC': u'ORBITAL CORP LIMITED',},
 '2520': {'BBG': u'BILLABONG',
          'FPA': u'FISHER & PAYKEL APP.',},
 '2530': {'ALL': u'ARISTOCRAT LEISURE',
          'CWN': u'CROWN LIMITED',
          'DMP': u'DOMINO PIZZA ENTERPR',
          'FLT': u'FLIGHT CENTRE',
          'GEM': u'G8 EDUCATION LIMITED',
          'JET': u'JETSET TRAVELWORLD',
          'NVT': u'NAVITAS LIMITED',
          'SGH': u'SLATER & GORDON',
          'SKC': u'SKY CITY ENTERTAIN.',
          'TAH': u'TABCORP HOLDINGS LTD',
          'TTS': u'TATTS GROUP LTD',
          'VEL': u'VEALLS LIMITED',},
 '2540': {'AAU': u'ADCORP AUSTRALIA',
          'APN': u'APN NEWS & MEDIA',
          'CMJ': u'CONSOLIDATED MEDIA.',
          'FXJ': u'FAIRFAX MEDIA LTD',
          'NWS': u'NEWS CORP',
          'PNW': u'PACIFIC STAR NETWORK',
          'SKT': u'SKY NETWORK',
          'SWM': u'SEVEN WEST MEDIA LTD',
          'SXL': u'STHN CROSS MEDIA',
          'TEN': u'TEN NETWORK HOLDINGS',
          'VRL': u'VILLAGE ROADSHOW LTD',},
 '2550': {'CCV': u'CASH CONVERTERS',
          'CTY': u'COUNTRY ROAD LIMITED',
          'DJS': u'DAVID JONES LIMITED',
          'HVN': u'HARVEY NORMAN',
          'JBH': u'JB HI-FI LIMITED',
          'KMD': u'KATHMANDU HOLD LTD',
          'MYR': u'MYER HOLDINGS LTD',
          'PBG': u'PACIFIC BRANDS',
          'TRS': u'THE REJECT SHOP',
          'VTG': u'VITA GROUP LTD',
          'WEB': u'WEBJET LIMITED',
          'WTF': u'WOTIF.COM HOLDINGS'},
 '3010': {'WES': u'WESFARMERS LIMITED',
          'WOW': u'WOOLWORTHS LIMITED'},
 '3020': {'BGA': u'BEGA CHEESE LTD',
          'CCL': u'COCA-COLA AMATIL',
          'ELD': u'ELDERS LIMITED',
          'GFF': u'GOODMAN FIELDER.',},
 '3030': {'BKL': u'BLACKMORES LIMITED'},
 '3510': {'ANN': u'ANSELL LIMITED',
          'FPH': u'FISHER & PAYKEL H.',
          'OMI': u'OMI HOLDINGS LIMITED',
          'PHG': u'PULSE HEALTH LIMITED',
          'SIP': u'SIGMA PHARMACEUTICAL',
          'VEI': u'VISION EYE INSTITUTE'},
 '3520': {'AVH': u'AVITA MEDICAL LTD',
          'LCT': u'LIVING CELL TECH.',
          'TIS': u'TISSUE THERAPIES',
          'VSC': u'VITA LIFE SCIENCES.'},
 '4010': {'ANZ': u'ANZ BANKING GRP LTD',
          'BEN': u'BENDIGO AND ADELAIDE',
          'BOQ': u'BANK OF QUEENSLAND.',
          'CBA': u'COMMONWEALTH BANK.',
          'NAB': u'NATIONAL AUST. BANK',
          'WBC': u'WESTPAC BANKING CORP'},
 '4020': {'AAY': u'AACL HOLDINGS LTD',
          'AEF': u'AUSTRALIAN ETHICAL',
          'APD': u'APN PROPERTY GROUP',
          'APP': u'APA FINANCIAL',
          'AQF': u'AUS GOV INDEX FUND',
          'ARG': u'ARGO INVESTMENTS',
          'ASX': u'ASX LIMITED',
          'CNG': u'COLONIAL HOLDING LTD',
          'IFL': u'IOOF HOLDINGS LTD',
          'MQG': u'MACQUARIE GROUP LTD',
          'SOL': u'(SOUL PATTINSON (W.H))',},
 '4030': {'AMP': u'AMP LIMITED',
          'QBE': u'QBE INSURANCE GROUP',
          'SBK': u'SUNCORP-METWAY .',
          'SUN': u'SUNCORP GROUP LTD',},
 '4040': {'CER': u'CENTRO RETAIL GROUP',
          'CRF': u'CENTRO RETAIL AUST',
          'GMG': u'GOODMAN GROUP',
          'LMW': u'LANDMARK WHITE LTD',
          'MGI': u'MACQUARIE GOODMAN',
          'MGM': u'MACQUARIE GOOD. MGT.',
          'MGR': u'MIRVAC GROUP',
          'MIX': u'MIRVAC INDUSTRIAL',
          'MUE': u'MULTIPLEX EUROPEAN',
          'MXU': u'MULTIPLEX SITES',
          'SGP': u'STOCKLAND',
          'WDC': u'WESTFIELD GROUP',
          'WFA': u'WESTFIELD AMERICA',
          'WFT': u'WESTFIELD TRUST',
          'WRT': u'WESTFIELD RETAIL TST',
          'WSF': u'WESTFIELD HOLDINGS',
          'WWM': u'WENTWORTH HLDGS LTD'},
 '4510': {'IFM': u'INFOMEDIA LTD',},
 '4520': {'AAT': u'AAT CORPORATION LTD',},
 '5010': {'SGT': u'SINGAPORE TELECOMM.',
          'TEL': u'TELECOM CORPORATION',
          'TLS': u'TELSTRA CORPORATION.',
          'TPC': u'TEL.PACIFIC LIMITED',},
 '5510': {'AGK': u'AGL ENERGY LIMITED',
          'HRL': u'HOT ROCK LIMITED',}
}


def get_time_series(firm_code):
    """This is the iterator you usually wish to call"""
    with gzip.open(get_time_series_file(firm_code), 'rb') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONE)
        for row in reader:
            yield row

def get_time_series_file(firm_code):
    cache_file_name = get_cache_file_name(firm_code)
    if not os.path.exists(cache_file_name):
        fetch_and_cache(firm_code)
    return cache_file_name

def get_cache_file_name(firm_code):
    return os.path.join(EQUITY_CACHE_DIR, firm_code + ".csv.gz")

def fetch_and_cache(firm_code):
    stock_data_request = requests.get(YAHOO_URL_TEMPLATE % firm_code)
    cache_file_name = get_cache_file_name(firm_code)
    with gzip.open(cache_file_name, 'wb') as cache_file:
        cache_file.write(stock_data_request.content)

def refresh_favourites_cache():
    for category, firm_dict in FAVOURITE_FIRMS.iteritems():
        for firm_code in firm_dict:
            fetch_and_cache(firm_code)

def refresh_all_cache():
    import asxinfo
    for category, firm_dict in asxinfo.ALL_INDUSTRY_FIRMS.iteritems():
        for firm_code in firm_dict:
            fetch_and_cache(firm_code)