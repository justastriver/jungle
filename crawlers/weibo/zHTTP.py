import requests


def get(url, encode='utf-8'):
      session = initSession()
      resp = session.get(url, allow_redirects=False)
      try:
	      redirect_url = resp.headers['location']
              #print "location: ", redirect_url
	      resp = session.get(redirect_url)
      except:
          print("err")
      try:
          txt = resp.text.encode(resp.encoding).decode(resp.apparent_encoding)
          return txt
      except:
          print('resp encode err')
	  return ''
      if encode == 'utf-8':
           return resp.text.encode(resp.encoding).decode(resp.apparent_encoding)
      return resp.text.encode("latin1").decode("gbk")#.encode(encode)

def initSession():
      session = requests.session()
      session.headers['User-Agent'] = (
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
      'Chrome/20.0.1132.57 Safari/536.11'
)
      #session.headers['referer'] = "https://image.baidu.com"
      return session



