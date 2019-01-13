import bs4

from spider import Spider
from weibo.weibo_message import WeiboMessage
import urllib 
import urllib2 
import requests
import os
import random

HOME_URL="https://www.biedoul.com/t/5bm96buY5Zu%2B54mH.html"

class CnbetaParser(Spider):
      def __init__(self):
            super(CnbetaParser, self).__init__(HOME_URL)

      def get_weibo_message(self):
            html = self.download_text()
            soup = bs4.BeautifulSoup( html, "html.parser" )
            items = soup.find_all( attrs={"class": "item"} )
            msg = ''
	    images = []
            if len( items ) > 0:
	       try:
                  topItem = items[random.randint(0, len(items)-1)]
#		  print topItem.a.string
                  title = topItem.a.string.strip()
                  path = topItem.a.get( 'href' )
                  #url = HOME_URL + path
		  url="https:"+path
                  #infodiv = topItem.find( attrs={"class": "newsinfo"} )
                  #content = infodiv.get_text()
		  imgurl=topItem.img.get('src')
#		  print imgurl
		  #filename="download/"+os.path.basename(imgurl)
		  #urllib.urlretrieve(imgurl,filename) 
		  #images.append(filename)
		  images.append(imgurl)
                  msg = "%s %s" % ( title, url )
	       except:
		  print "errer "
            return WeiboMessage( msg,images)
