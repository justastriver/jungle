from threading import Thread, Event

import random
import time
import db
import json

from config import TIME_SLOG
from weibo.weibo_sender import WeiboSender
from weibo.weibo_message import WeiboMessage
from logger import logger

class SendTask(Thread):
      def __init__(self, http, uid):
            Thread.__init__(self)
            self.stopped = Event()
            self.sender = WeiboSender( http, uid )
	    self.md5 = ''

      def run(self):
            logger.info( "start task..." )
            if True == self.sendWeibo():
	         logger.info("send ok...")
	         db.update(self.md5)
            #while not self.stopped.wait(TIME_SLOG):
            while not self.stopped.wait(random.randint(1,3) * TIME_SLOG):
                  if True == self.sendWeibo():
		      logger.info("send ok...")
		      db.update(self.md5)
		  logger.info("repeat cause false,")
            logger.info( "end task..." )

      def stop(self):
            self.stopped.set()

      def get_weibo_message(self):
	  res = db.getOne()
	  if res is None:
	  	print res
	  	logger.info('none crawler content')
	  	return None
	  print res[0],res[1],res[2],res[3],res[4],res[5]
	  self.md5 = res[4]
	  content = res[1]
	  images = res[2].split(' ')
	  weibo = WeiboMessage(content,images)
	  return weibo

      def sendWeibo(self):
	    try:
                weibo = self.get_weibo_message()
	        if weibo is None:
		   return False
		else:
                   return self.sender.send_weibo(weibo)
	    except:
		logger.info("error to get weibo message")
		return False
	    return True
