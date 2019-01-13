import zHTTP
from datetime import datetime
import db
import json
from logger import logger

class Spider(object):
      '''spider base class'''
      def __init__(self, homeUrl):
            super(Spider, self).__init__()
            self.homeUrl = homeUrl

      def download_text(self, encode = 'utf-8'):
            '''get raw text such as html,json,or so on'''
            text = zHTTP.get( self.homeUrl,encode )
            return text
      def get_html(self, url, encode = 'utf-8'):
	      return zHTTP.get(url, encode)

      def get_weibo_message(self):
            pass
      def make_json(self, title, content, images, link):
	      js = {'title':title.replace('"',''),'content':content.replace('"',''),'link':link,'images':images}
	      return json.dumps(js)

      def save(self, title, content, images, link, source):
	  db.insert_new_pub_context(title, content,images,link,source)
	  #res = db.getOne()
	  #print json.loads(res[0])

