# coding: utf-8
import bs4
import random
import re
import requests
import json
import urllib
import jieba.posseg as pseg
import sys 
sys.path.append("..") 

from spider import Spider
#from weibo.weibo_message import WeiboMessage
from config import callback_url

HOME_URL = "https://s.weibo.com/top/summary?cate=realtimehot"

class WeiboHotParser(Spider):
      def __init__(self):
            super(WeiboHotParser, self).__init__(HOME_URL)

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

      def get_tags_array(self, keyword):
          words = pseg.cut(keyword)
	  tags = []
	  tags.append(keyword)
          for word, flag in words:
	      if flag == 'nz' or flag == 'nr' or flag == 'ns' or flag == 'nt':
		 tags.append(word)
	  return tags

      def make_tags(self, tags):
	  tag_str = ''
	  for tag in tags:
	      tag = ' #%s# ' % tag 
	      tag_str = tag
	  #print tag_str
	  return tag_str
	      

      def get_weibo_message(self):
            html = self.download_text(encode='utf-8')
            soup = bs4.BeautifulSoup( html, "html.parser" )
            div = soup.find(attrs={"class":"data"})
            items = div.find_all( 'tr' )
            msg = ''
            images = []
            if len( items ) > 1:
	       for i in range(len(items)):
                  idx=random.randint(1,len(items)-1)
                  topItem = items[idx]
                  #print("random:",idx, len(items))
                  try:
			keyword = topItem.find(attrs={"class":"td-02"}).a.get_text().strip()
                        kwditem = topItem.find(attrs={"class":"td-03"})
			print keyword
			arr = self.get_tags_array(keyword)
	                query_word = ''
	                if len(arr) > 1:
			    query_word = arr[1]
			    print 'query:',query_word
			else:
			    query_word = arr[0]
			    continue
			pic_urls ,title ,from_url = self.get_image_urls(query_word.encode('utf-8'))
                  	#msg = "%s %s" % ( title, src_url )
                        tags = self.make_tags(arr)
			emo = u"[围观][围观]"
			from_url = "%s%s" % (callback_url,from_url)
                  	msg = "%s , %s %s, %s" % (tags, title ,emo, from_url)
			images = pic_urls
			print(msg)
		        break
		  except:
		  	print "error...,continue .."
            #return WeiboMessage( msg , images)

if __name__ == '__main__':
        spider = WeiboHotParser()
        spider.get_weibo_message()
        #spider.test()
        #spider.get_image_urls('海底捞播不雅画面')
