# coding: utf-8
import bs4
import random
import re
import requests
import json
import urllib


if __name__ == '__main__':
              keyword='美人鱼'
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
              html = requests.get(url,headers=headers).text
              dataList = json.loads(html)
	      #print dataList
              for i in dataList.get('data'):
                        if i.get('thumbURL') != None:
                             #print('image url:%s' % i.get('thumbURL'))
			     images.append(i.get('thumbURL'))
                        if i.get('fromPageTitleEnc') != None:
                             #print('title: %s' % i.get('fromPageTitleEnc').encode('utf-8'))
			     if len(title) < len(i.get('fromPageTitleEnc')):
			        title = i.get('fromPageTitleEnc')
                        if i.get('fromURLHost') != None:
                             print('from: %s' %  i.get('fromURLHost'))
			     if from_host== '':
			        from_host= i.get('fromURLHost')
                        if i.get('replaceUrl') != None:
                             for j in i.get('replaceUrl'):
                                 if j.get('FromURL') != None:
                                    #print('from: %s' %  j.get('FromURL'))
			     	    if from_url == '':
			        	from_url = j.get('FromURL')
					break


              print from_host, from_url
	      from_url = "http://" + from_url

