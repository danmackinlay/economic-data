# http://www.stat.berkeley.edu/~nolan/stat133/Fall05/lectures/SQL-R.pdf

library("foreign")
library("RSQLite")

years = sprintf("%02d", (62:100 %% 100))

read.one.wtf = function() {
  wtf = read.dta("/Users/dan/Desktop/researchtmp/un/wtf62.dta")

  m <- dbDriver("SQLite")
  con <- dbConnect(m, dbname = "wtf.db")
  dbWriteTable(con, "wtf", wtf, append=TRUE)
  on.exit(dbDisconnect(con))
}

read.one.wtf()

#dbBuildTableDefinition
