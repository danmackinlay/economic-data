base.path = '/Users/dan/Dropbox/trade_data/cache/'
files = list.files(base.path, pattern=".*\\.csv\\.gz")

i=0
limit=10

equities = data.frame()

for (file.name in files) {
  ticker.name = substr(file.name, 1, 3)
  i=i+1
  print(ticker.name)
  print(paste(base.path, file.name, sep = ""))
  one.equity = read.csv(gzfile(paste(base.path, file.name, sep = "")))
  trimmed.equity = one.equity[c("Date")]
  trimmed.equity[ticker.name] = log(one.equity["Adj.Close"])
  if(i>limit) {break}
  rm(one.equity)
  equities = merge(equities, trimmed.equity, all.x=TRUE, all.y=TRUE)
}