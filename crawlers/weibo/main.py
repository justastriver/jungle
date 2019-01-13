# -*- coding: utf-8 -*-

import send_task
import spider_factory

if __name__ == '__main__':
    spider_num=len(spider_factory.spiders)
    for i in xrange(spider_num):
        task =  send_task.SendTask(i)
        task.start()
        #task.stop()
    
