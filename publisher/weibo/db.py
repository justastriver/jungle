from threading import Thread, Event

import random

from config import db_name
from config import db_host
from config import db_port
from config import db_pwd
from config import db_table
from config import db_user
from logger import logger
import hashlib
import pymysql

#pub_content_list(id int, context text,md5 text,pub_time datetime);
def connect_wxremit_db():
	    return pymysql.connect(host=db_host,
				    port=db_port,
				    user=db_user,
				    password=db_pwd,
				    database=db_name,
				    charset='utf8')

#res = db.getOne()
#print res
#print json.loads(res[0])
def getOne(source=''):
        sql_str = ("SELECT title, context, images, link,md5, source"
                 + " FROM " + db_table
                 + " WHERE status != 1 order by pub_time desc limit 1" )
	if source != '':
              sql_str = ("SELECT title, context, images, link, md5, source"
                 + " FROM " + db_table
                 + " WHERE status != 1 and source = '%s' order by pub_time desc limit 1" % (source) )

        #logger.debug(sql_str)

        con = connect_wxremit_db()
	cur = con.cursor()
        cur.execute(sql_str)
	row = cur.fetchone()
	cur.close()
	con.close()

	return row

def update(cc2):
        sql_str = ("update %s set status = 1  WHERE md5='%s'" % (db_table, cc2))
        #logger.debug(sql_str)

        con = connect_wxremit_db()
	cur = con.cursor()
        cur.execute(sql_str)
	rows = cur.fetchall()
	cur.close()
	con.close()

	if len(rows) == 1:
		return True
	return False


def is_published(cc2):
        sql_str = ("SELECT status"
                 + " FROM " + db_table
                 + " WHERE md5='%s'" % (cc2))
        #logger.debug(sql_str)

        con = connect_wxremit_db()
	cur = con.cursor()
        cur.execute(sql_str)
	rows = cur.fetchall()
	cur.close()
	con.close()

	if len(rows) == 1:
		return True
	return False

def insert_new_pub_context(title, content, images,link, source):

	md5data = hashlib.md5(content.encode('utf-8')).hexdigest()
	if is_published(md5data) == True:
	   #logger.info("already published")
	   return
	con = connect_wxremit_db()
	cur = con.cursor()
	try:
		sql_str = ("INSERT INTO %s (title, context,images,link, source, md5)  VALUES ('%s', '%s','%s', '%s','%s','%s')" % (db_table,title,content,images,link,source, md5data))
	        cur.execute(sql_str)
	        con.commit()
	except Exception as e:
		con.rollback()
		logger.debug('Insert operation error %s' % (e))
		raise
	finally:
	        cur.close()
	        con.close()
