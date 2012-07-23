# Two granger libraries - we use the latter because it has missing value handling baked in,
# though the former is better for vectorised correlations
# Note that neither support true multivariate calculations, just pairwise.
#library("MSBVAR")
library("lmtest")
#library("ggplot2")
library("reshape2")
#library("ggdendro")
library("RSQLite")

# example usage:
# equities = pairwise.granger.test(get.favourite.indices(limit=Inf))
# #equities.m = pairwise.granger.test.m(get.favourite.indices(limit=Inf))


base.path = '/Users/dan/Dropbox/trade_data'
cache.path = paste(base.path, "cache", sep="/")

get.favourite.equities = function (limit=10) {
  files = list.files(cache.path, pattern=".*\\.csv\\.gz")
  favourite.equities.ticker.names = c('AAI', 'AAT', 'AAU', 'AAY', 'AEF', 'AGK', 'AIZ', 'ALL', 'AMP', 'ANN', 'ANZ', 'APD', 'APN', 'APP', 'AQF', 'ARG', 'ASX', 'AVH', 'BBG', 'BEN', 'BGA', 'BHP', 'BKL', 'BOQ', 'BXB', 'CBA', 'CCL', 'CCV', 'CER', 'CLO', 'CLX', 'CMJ', 'CNG', 'CRF', 'CSR', 'CTY', 'CWN', 'CYU', 'DJS', 'DMP', 'EAU', 'ELD', 'FLT', 'FMG', 'FPA', 'FPH', 'FXJ', 'GDA', 'GEM', 'GFF', 'GMG', 'HRL', 'HVN', 'IFL', 'IFM', 'ION', 'JBH', 'JET', 'KMD', 'LCT', 'LMW', 'MGI', 'MGM', 'MGR', 'MIX', 'MQG', 'MUE', 'MXU', 'MYR', 'NAB', 'NCM', 'NVT', 'NWS', 'OEC', 'OMI', 'ORD', 'ORG', 'ORI', 'OST', 'PBG', 'PHG', 'PNW', 'QAN', 'QBE', 'QRN', 'RRS', 'RUM', 'SBK', 'SGH', 'SGP', 'SGT', 'SIP', 'SKC', 'SKT', 'SOL', 'SUN', 'SWM', 'SXL', 'SYD', 'TAH', 'TEL', 'TEN', 'TIS', 'TLS', 'TPC', 'TRS', 'TSE', 'TTS', 'VEI', 'VEL', 'VRL', 'VSC', 'VTG', 'WBC', 'WDC', 'WEB', 'WES', 'WFA', 'WFT', 'WOW', 'WRT', 'WSF', 'WTF', 'WWM', 'ZBI', 'ZRI')
  i=0

  equities = NULL;

  for (file.name in files) {
    ticker.name = substr(file.name, 1, 3)
  
    if(!(ticker.name %in% favourite.equities.ticker.names)) {next}
    if(i>limit) {break}
    
    i=i+1
      
    one.equity = read.csv(gzfile(paste(cache.path, file.name, sep = "/")))
    trimmed.equity = one.equity[c("Date")]
    #take max because some shares still trade at 0 (granularity is $0.01, zero is -4.61)
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

# This looks like it should go formula style.
# grangertest(AAT ~ AAY, data=equities)
# but constructing formulae in code is tedious,
# so we pass time series directly

get.ts = function(equities, ticker.name) {
  return(zoo(equities[,ticker.name], equities$Date))
}

granger.fp = function(xname, yname, data, order=1){
  res = NULL
  error = try(res <- grangertest(data[,xname], data[,yname], order=order))
  if(is.null(res)) return(list(F=NA,P=NA,worked=FALSE))
  f = res[2, "F"]
  p = res[2, "Pr(>F)"]
  return(list(F=f, P=p, worked=TRUE))
}
vec.granger.fp = Vectorize(granger.fp, vectorize.args=c('xname', 'yname'))

granger.p = function(xname, yname, data, order=1){
  return(as.numeric(granger.fp(xname, yname, data, order)['P']))
}
vec.granger.p = Vectorize(granger.p, vectorize.args=c('xname', 'yname'))

granger.f = function(xname, yname, data, order=1){
  return(as.numeric(granger.fp(xname, yname, data, order)['F']))
}
vec.granger.f = Vectorize(granger.f, vectorize.args=c('xname', 'yname'))

# returns a "melted" pairwise granger-causality distance frame
#Need to cast this to and from p/f matrices
#try:
# http://stackoverflow.com/a/9617424
# http://tolstoy.newcastle.edu.au/R/e6/help/09/01/0598.html
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
  
  #danger! this ignores the asymmetry of the relation!
  for(j in 1:(n-1)) {
    for(k in (j+1):(n)) {
      left.name = equity.names[j]
      right.name = equity.names[k]
      print(c(left.name, right.name))
      res = granger.fp(left.name, right.name, equities, order)
      i = i+1
      lefts[i] = left.name
      rights[i] = right.name
      fs[i] = res$F
      ps[i] = res$P
      res = granger.fp(right.name, left.name, equities, order)
      i = i+1
      lefts[i] = right.name
      rights[i] = left.name
      fs[i] = res$F
      ps[i] = res$P
    }
  }
  return(data.frame(left=as.factor(lefts), right=as.factor(rights), F=fs, P=ps))
}

# returns a pairwise granger-causality distance matrix
# Need to cast this to and from sparse p/f frames
pairwise.granger.test.m = function(equities, order=1) {
  x = names(equities)[-1]
  names(x) = x
  y = x
  return(outer(x, y, vec.granger.f, equities))
}

#To see how to do this, try...
#  Traditional:
#    http://flowingdata.com/2010/01/21/how-to-make-a-heatmap-a-quick-and-easy-solution/
#    http://sphaerula.com/legacy/R/correlationPlot.html
#    http://www.phaget4.org/R/image_matrix.html
#  ggplot2:
#    https://learnr.wordpress.com/2010/01/26/ggplot2-quick-heatmap-plotting/
#    http://stackoverflow.com/a/5554352
#    http://stackoverflow.com/a/6675983 (bonus dendrogram!)
#    http://hosho.ees.hokudai.ac.jp/~kubo/Rdoc/library/ggmap/html/ggimage.html
#  general community structure:
#    http://sieste.wordpress.com/2012/05/21/inferring-the-community-structure-of-networks/
#    http://cran.cnr.berkeley.edu/web/views/Cluster.html
#
# linkcomm seems to do this for weighted digraphs.
# agnes (from cluster) doesn't like missing values, hclust (from stats) might be OK with 'em, but it isn't clear
# Here is an R GEXF gephi exporter (although a CSV export will probably do the trick)
# Drew conway chatter on the issue: http://www.drewconway.com/zia/?p=1221
# For a combo version, use the r heatmap plot with bonus dendrogram
#   heatmap(favourite.pairwise.vals)
#   more general clustering is in PDM, cluster, et al
# Sorting each axis separately might be informative enough without getting overexcited about directed graphs. 
# probably it can all go into SQL anyway

plot.correlation.matrix = function(correlations){
  
}

# For SQL, gephi likes nodes and edges in separate tables - 
# Edges:
# "source", "target", "label", "weight"
# Nodes:
# "id", "label", "x, "y", "size"
# For both of these we can add "start" and "end" to dynamic graphs

# Convert a sparse pairwise correlation frame into a weighted, directed,
# SQL graph
correlation.to.sql = function(data, dbname="equities_graph.db") {
  conn <- dbConnect("SQLite", dbname = paste(base.path, dbname, sep="/"))

  ## The interface can work at a higher level importing tables 
  ## as data.frames and exporting data.frames as DBMS tables.

  dbListTables(con)
  dbListFields(con, "quakes")
  if(dbExistsTable(con, "new_results"))
    dbRemoveTable(con, "new_results")
  dbWriteTable(con, "new_results", new.output)
  
  ## The interface allows lower-level interface to the DBMS
  res <- dbSendQuery(con, paste(
    "SELECT g.id, g.mirror, g.diam, e.voltage",
    "FROM geom_table as g, elec_measures as e",
    "WHERE g.id = e.id and g.mirrortype = 'inside'",
    "ORDER BY g.diam"))
  out <- NULL
  while(!dbHasCompleted(res)){
    chunk <- fetch(res, n = 10000)
    out <- c(out, doit(chunk))
  }

  ## Free up resources
  dbClearResult(res)
  dbDisconnect(con)
  dbUnloadDriver(drv)

  rs <- dbSendQuery(con, statement = paste(
    "SELECT w.laser_id, w.wavelength, p.cut_off",
    "FROM WL w, PURGE P",
    "WHERE w.laser_id = p.laser_id", 
    "SORT BY w.laser_id"))
  data <- fetch(rs, n = -1)   # extract all rows                  
}