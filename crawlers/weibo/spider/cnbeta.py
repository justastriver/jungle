import bs4

from spider import Spider
import urllib 
import urllib2 
import requests
import os
import random
from config import callback_url

#HOME_URL = "http://www.cnbeta.com"
#HOME_URL = "https://www.cnbeta.com/category/funny.htm"
#HOME_URL = "https://www.cnbeta.com/category/comic.htm"
HOME_URL="https://www.cnbeta.com/category/movie.htm"

class CnbetaParser(Spider):
      def __init__(self):
            super(CnbetaParser, self).__init__(HOME_URL)

      def get_weibo_message(self):
            html = self.download_text()
            soup = bs4.BeautifulSoup( html, "html.parser" )
            items = soup.find_all( attrs={"class": "item"} )
            msg = ''
	    images = []
	    for item in items:
	       try:
#		  print topItem.a.string
                  title = item.a.string.strip()
                  path = item.a.get( 'href' )
                  #url = HOME_URL + path
		  url="https:"+path
		  from_url = "%s%s" % (callback_url,url)
                  #infodiv = item.find( attrs={"class": "newsinfo"} )
                  #content = infodiv.get_text()
		  imgurl=item.img.get('src')
#		  print imgurl
		  #filename="download/"+os.path.basename(imgurl)
		  #urllib.urlretrieve(imgurl,filename) 
		  #images.append(filename)
		  images.append(imgurl)
                  msg = "%s %s" % ( title, from_url )
		  #content=self.make_json(title, msg, images, from_url)
	          #logger.info(content)
		  self.save(title, msg, ' '.join(images), from_url, 'cnbeta')
	       except:
		  print "errer "
