from bs4 import BeautifulSoup as bs
import requests
from config import *


import musixmatch
apikey = '7c743be888303b3454a66a6d798361a1'
try:
    chart = musixmatch.ws.track.chart.get(country='it', apikey=apikey)
except musixmatch.api.Error as e:
    pass
