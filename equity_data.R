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

get.ts = function(equities, ticker.name) {
  return(zoo(equities[,ticker.name], equities$Date))
}

granger.fp = function(data, xname, yname, order){
  res = NULL
  error = try(res <- grangertest(data[,xname], data[,yname], order=order))
  if(is.null(res)) return(list(F=NA,P=NA,worked=FALSE))
  f = res[2, "F"]
  p = res[2, "Pr(>F)"]
  return(list(F=f, P=p, worked=TRUE))
}

pairwise.granger.test = function(equities, order=1) {
  equity.names = names(equities)[-1]
  n = length(equity.names)
  n.pairs = n*(n-1)
  relations = data.frame
  lefts = vector(mode='character', length = n.pairs)
  rights = vector(mode='character', length = n.pairs)
  fs = vector(mode='numeric', length = n.pairs)
  ps = vector(mode='numeric', length = n.pairs)
  i = 0
  for(j in 1:(n-1)) {
    for(k in (j+1):(n)) {
      left.name = equity.names[j]
      right.name = equity.names[k]
      print(c(left.name, right.name))
      res = granger.fp(equities, left.name, right.name, order)
      i = i+1
      lefts[i] = left.name
      rights[i] = right.name
      fs[i] = res$F
      ps[i] = res$P
      res = granger.fp(equities, right.name, left.name, order)
      i = i+1
      lefts[i] = right.name
      rights[i] = left.name
      fs[i] = res$F
      ps[i] = res$P
    }
  }
  return(data.frame(left=as.factor(lefts), right=as.factor(rights), F=fs, P=ps))
}