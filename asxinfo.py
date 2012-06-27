import requests
from bs4 import BeautifulSoup

"""From view-source:http://www.asx.com.au/asx/research/companyInfo.do we know that these are the GICS codes lised on the ASX."""

ASX_INDUSTRIES = {
    "2510": "Automobile & Components",
    "4010": "Banks",
    "2010": "Capital Goods",
    "2020": "Commercial & Professional Services",
    "2520": "Consumer Durables & Apparel",
    "2530": "Consumer Services",
    "4020": "Diversified Financials",
    "1010": "Energy",
    "3010": "Food & Staples Retailing",
    "3020": "Food Beverage & Tobacco",
    "3510": "Health Care Equipment & Services",
    "3030": "Household & Personal Products",
    "4030": "Insurance",
    "1510": "Materials",
    "2540": "Media",
    "3520": "Pharmaceuticals, Biotechnology & Life Sciences",
    "4040": "Real Estate",
    "2550": "Retailing",
    "4530": "Semiconductors & Semiconductor Equipment",
    "4510": "Software & Services",
    "4520": "Technology Hardware & Equipment",
    "5010": "Telecommunication Services",
    "2030": "Transportation",
    "5510": "Utilities",
}

"""For each GICS code we may extract a list of appropriate companies at a URL like
http://www.asx.com.au/asx/research/companyInfo.do?by=industryGroup&industryGroup=2530
Then we look for a lsit of companies ina a "select" field named "asxCode".
"""
GICS_URL_TEMPLATE = "http://www.asx.com.au/asx/research/companyInfo.do?by=industryGroup&industryGroup=%s"

industries = {}

def get_codes():
    global industries
    for gics_code in ASX_INDUSTRIES.keys():
        companies = {}
        r = requests.get(GICS_URL_TEMPLATE % gics_code)
        bs=BeautifulSoup(r.content)
        company_fields = bs.find("select", {'name':"asxCode"}).findAll("option")
        for company in company_fields:
            companies[company.attrs['value']] = company.text
        industries[gics_code] = companies
    return industries
        
    