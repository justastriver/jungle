from threading import Thread, Event

import spider_factory
import random
import time

from config import TIME_SLOG
from logger import logger

class SendTask(Thread):
      def __init__(self, idx):
            Thread.__init__(self)
            self.stopped = Event()
	    self.idx = idx

      def run(self):
            logger.info( "start task..." )
            while not self.stopped.wait(TIME_SLOG):
                    spider = spider_factory.getSpider(self.idx)
                    weibo = spider.get_weibo_message()

            logger.info( "end task..." )

      def stop(self):
            self.stopped.set()
            
