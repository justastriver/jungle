from spider.cnbeta import CnbetaParser
#from spider.cnblog import CnblogParser
#from spider.miaopai import MiaopaParser
#from spider.myBlog import MyBlogParser
from spider.techweb import TechwebParser
#from spider.tuicool import TuicoolParser
from spider.baiduHot import BaiduHotParser
from spider.baiduHotEnt import BaiduHotEntParser

spiders = [ 
          #BaiduHotEntParser() ,
#          MyBlogParser(),
          CnbetaParser(),
#          CnblogParser(),
#          MiaopaParser(),
#          MyBlogParser(),
#          TuicoolParser() 
          BaiduHotParser(),
          TechwebParser()
        ]


def getSpider(idx):
      spider = spiders[idx]
      return spider
