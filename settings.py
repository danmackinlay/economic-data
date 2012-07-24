import os.path

EQUITY_BASE_DIR = os.path.expanduser('~/Dropbox/trade_data')
EQUITY_CACHE_DIR = os.path.join(EQUITY_BASE_DIR, 'cache')

try:
	from _local_settings import *
except ImportError:
	pass
