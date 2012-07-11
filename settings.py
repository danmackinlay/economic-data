import os.path
try:
	import _local_settings
except ImportError:
	pass

EQUITY_CACHE_DIR = os.path.expanduser('~/Dropbox/trade_data/cache')
