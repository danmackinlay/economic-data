import os.path

EQUITY_CACHE_DIR = os.path.expanduser('~/Dropbox/trade_data/cache')

try:
	from _local_settings import *
except ImportError:
	pass
