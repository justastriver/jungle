import bs4
import random

from spider import Spider
from config import callback_url
from logger import logger

HOME_URL = "http://www.techweb.com.cn/roll"

class TechwebParser(Spider):
      def __init__(self):
            super(TechwebParser, self).__init__(HOME_URL)

      def get_weibo_message(self):
            html = self.download_text()
            soup = bs4.BeautifulSoup( html, "html.parser" )
            div = soup.find( attrs={ "class": "newslist" } )
            items = div.ul.find_all( 'li' )
            msg = ''
	    for item in items:
		  try:
                  	title = item.a.string.strip()
                  	url = item.a.get( 'href' )
			from_url = "%s%s" % (callback_url,url)
                  	msg = "%s %s" % ( title, from_url )
			images=[]
			#content=self.make_json(title, msg, images, from_url)
	                logger.info(content)
			self.save(title, msg, ' '.join(images),from_url, 'techweb')
		  except:
		  	print "techweb error...,continue .."
