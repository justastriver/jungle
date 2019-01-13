# coding: utf-8
import bs4
import random
import re
import requests
import json
import urllib
import jieba.posseg as pseg
import time

from spider import Spider
from config import callback_url

HOME_URL = "http://top.baidu.com/buzz?b=1&c=513&fr=topbuzz_b1_c513"
#HOME_URL = "http://image.baidu.com/search/index?tn=baiduimage&lm=-1&ct=201326592&cl=2&word=%B0%C2%C0%AD%B5%CF%B2%A8%D7%BC%BE%F8%C9%B1&ie=gbk"

class BaiduHotParser(Spider):
      def __init__(self):
            super(BaiduHotParser, self).__init__(HOME_URL)

      def get_image_urls(self,keyword):
	      images= []
	      title = ''
	      from_url = ''
	      from_host= ''
              html=''
              headers = \
			    {
			         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
				      "referer":"https://image.baidu.com"
				          }

              url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={word}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=girl&pn={pageNum}&rn=30&gsm=1e00000000001e&1490169411926="
              keyword = urllib.quote(keyword,"utf-8")
              n = 1
              url = url.format(word=keyword,pageNum=str(n))
              #rep=urllib.request.Request(url,headers=header)
              #rep=urllib.request.urlopen(rep)
              html = self.get_html(url)#requests.get(url,headers=headers).text
              dataList = json.loads(html)
	      #print dataList
              for i in dataList.get('data'):
                        if i.get('thumbURL') != None:
                             #print('image url:%s' % i.get('thumbURL'))
			     images.append(i.get('thumbURL'))
                        if i.get('fromPageTitleEnc') != None:
                             #print('title: %s' % i.get('fromPageTitleEnc').encode('utf-8'))
			     if len(title) < len(i.get('fromPageTitleEnc')):
			     #if title == '':
			        title = i.get('fromPageTitleEnc')
                        if i.get('fromURLHost') != None:
                             #print('from: %s' %  i.get('fromURLHost'))
			     if from_host== '':
			        from_host= i.get('fromURLHost')
                        if i.get('replaceUrl') != None:
                             for j in i.get('replaceUrl'):
                                 if j.get('FromURL') != None:
                                    #print('from: %s' %  j.get('FromURL'))
			     	    if from_url == '':
			        	from_url = j.get('FromURL')
					break


	      if from_url == '':
	         from_url = from_host
              print title, from_host, from_url
	      if 'http' not in from_url:
	          from_url = "http://" + from_url
              return images,title, from_url

      def get_tags(self, keyword):
          words = pseg.cut(keyword)
	  tags = '#%s# ' % keyword
          for word, flag in words:
	      if flag == 'nz' or flag == 'nr' or flag == 'ns' or flag == 'nt':
		   tag = ' #%s# ' % word
		   tags = tags + tag
	  return tags

      def get_weibo_message(self):
            html = self.download_text(encode='utf-8')
            soup = bs4.BeautifulSoup( html, "html.parser" )
            div = soup.find(attrs={"class":"grayborder"})
	    #print div
	    #table = div.table
            items = div.find_all( 'tr' )
            msg = ''
            images = []
	    for topItem in items:
                  try:
                        kwditem = topItem.find(attrs={"class":"keyword"})
			keyword = kwditem.find(attrs={"class":"list-title"}).get_text().strip()
			linkItem = topItem.find(attrs={"class":"tc"}).find_all('a')
			newsUrl = linkItem[0].get('href')
			videoUrl = linkItem[1].get('href')
			picUrl = linkItem[2].get('href')
			print keyword
			#print("get image url:" + picUrl)
			#picUrl = "http://image.baidu.com/i?tn=baiduimage&lm=-1&ct=201326592&cl=2&word=%B7%AD%D2%EB%BC%D2%D5%C5%D3%F1%CA%E9%C8%A5%CA%C0&ie=gbk"
			pic_urls ,title ,from_url = self.get_image_urls(keyword.encode('utf-8'))
                  	#msg = "%s %s" % ( title, src_url )
                        tags = self.get_tags(keyword)
			emo = u"[围观][围观]"
			from_url = "%s%s" % (callback_url,from_url)
                  	msg = "%s , %s %s, %s" % (tags, title ,emo, from_url)
			images = pic_urls
			#content=self.make_json(title, msg, images, from_url)
			self.save(title,msg,' '.join(images), from_url,'baiduhot')
			logger.info(content)
			print(msg)
		  except:
		  	print "error...,continue .."
		  time.sleep(5)

if __name__ == '__main__':
        spider = BaiduHotParser()
        spider.get_weibo_message()
        #spider.test()
        #spider.get_image_urls('海底捞播不雅画面')
