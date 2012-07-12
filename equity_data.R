# Two granger libraries - we use the latter because it has missing value handling baked in,
# though the former is better for pairwise tables
#library("MSBVAR")
library("lmtest")

base.path = '/Users/dan/Dropbox/trade_data/cache/'

get.favourite.indices = function (limit=10) {
  
  files = list.files(base.path, pattern=".*\\.csv\\.gz")
  favourite.equities.ticker.names = c('AAI', 'AAT', 'AAU', 'AAY', 'AEF', 'AGK', 'AIZ', 'ALL', 'AMP', 'ANN', 'ANZ', 'APD', 'APN', 'APP', 'AQF', 'ARG', 'ASX', 'AVH', 'BBG', 'BEN', 'BGA', 'BHP', 'BKL', 'BOQ', 'BXB', 'CBA', 'CCL', 'CCV', 'CER', 'CLO', 'CLX', 'CMJ', 'CNG', 'CRF', 'CSR', 'CTY', 'CWN', 'CYU', 'DJS', 'DMP', 'EAU', 'ELD', 'FLT', 'FMG', 'FPA', 'FPH', 'FXJ', 'GDA', 'GEM', 'GFF', 'GMG', 'HRL', 'HVN', 'IFL', 'IFM', 'ION', 'JBH', 'JET', 'KMD', 'LCT', 'LMW', 'MGI', 'MGM', 'MGR', 'MIX', 'MQG', 'MUE', 'MXU', 'MYR', 'NAB', 'NCM', 'NVT', 'NWS', 'OEC', 'OMI', 'ORD', 'ORG', 'ORI', 'OST', 'PBG', 'PHG', 'PNW', 'QAN', 'QBE', 'QRN', 'RRS', 'RUM', 'SBK', 'SGH', 'SGP', 'SGT', 'SIP', 'SKC', 'SKT', 'SOL', 'SUN', 'SWM', 'SXL', 'SYD', 'TAH', 'TEL', 'TEN', 'TIS', 'TLS', 'TPC', 'TRS', 'TSE', 'TTS', 'VEI', 'VEL', 'VRL', 'VSC', 'VTG', 'WBC', 'WDC', 'WEB', 'WES', 'WFA', 'WFT', 'WOW', 'WRT', 'WSF', 'WTF', 'WWM', 'ZBI', 'ZRI')
  i=0

  equities = NULL;

  for (file.name in files) {
    ticker.name = substr(file.name, 1, 3)
  
    if(!(ticker.name %in% favourite.equities.ticker.names)) {next}
    if(i>limit) {break}
    
    i=i+1
      
    one.equity = read.csv(gzfile(paste(base.path, file.name, sep = "")))
    trimmed.equity = one.equity[c("Date")]
    #take max because some share trade at 0 (granularity is $0.01, zero is -4.61)
    trimmed.equity[ticker.name] = log(pmax(
      one.equity["Adj.Close"],
      0.005))

    if(is.null(equities)) {
      equities = trimmed.equity
    } else {
      equities = merge(equities, trimmed.equity, all.x=TRUE, all.y=TRUE)
    }
  }
  equities$Date = as.Date(equities$Date)
  return(equities)
}

# this looks like it should go, formula style.
# grangertest(AAT ~ AAY, data=equities)
# so we go for time series

get.ts.from.equities = function(equities, ticker.name) {
  return(zoo(equities[,ticker.name], equities$Date))
}

get.all.granger.test = function(equities) {
  n.equities = length(names(equities)) - 1
  n.pairs = n(n-1)/2
  
}