=============
economic-data
=============

parse some economic data sets  that i have on hand

Todo
====

* Data is not correctly normalised for a DB but rather is in pre-joined tables as fits a stats
  program. Normalise it better.

Questions
=========

Scientific
----------

* What is the best metric to use to look for clusters or their absence?

  * Innovation?
  * Quantity of goods moved?
  * Patents filed?

* How do you "cost" developing a new technology? No centralised records of such things are kept
* Time dimension. How do we deal with the dynamic qualities of these networks?
* Is it worthwhile reproducing Hidalgo and Hausmann's work, or simply starting anew with new
  metrics?

Technical
---------

* geocoding. How to quantify actual locations of the addresses, and distances between them.
* how to stitch together the addresses of companies.
* UN SITC database is not available in a plaintext of spreadsheet format but may be parsed off
  their website, given a day or two.
* US databases are by far the best represented. Is this sufficient?

  * SEC has some data although may only have addresses for the top 10000 publicly traded
    companies http://www.sec.gov/edgar/searchedgar/webusers.htm - appears to require manual data
	scraping.
  * Aswath Damodaran has some valuation data sets, US back a decade and global since this year.
    http://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html
  * nonNBER-santisied papaten data at http://patft.uspto.gov/help/contents.htm


