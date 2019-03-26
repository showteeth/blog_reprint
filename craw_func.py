import re
import os
import argparse
import logging
logging.basicConfig(level=logging.DEBUG,format="%(levelname)s-%(filename)s:[%(lineno)d]-%(message)s")
import requests
from bs4 import BeautifulSoup
from lxml import etree

# parse pages use beautifulsoup
# this is not easy to expand, so I use xpath instead
def craw_func_bs(url,content_id):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    logging.info("start parse info from {}".format(url))
    try:
        res = requests.get(url,headers=headers,timeout=200)
        soup = BeautifulSoup(res.text,'html.parser')
    except:
    	# 找不到或者网页有问题跑出错误
    	raise ValueError('page error')
    if res.status_code == 200:
    	logging.info("start get interested content")
    	content=soup.find_all(id='{}'.format(content_id))
    	title=test
    	if len(content)!=0:
    		return str(content[0])
    	else:
    		raise ValueError('page is empty, please check the content_id you use')
# content=craw_func(url,'cnblogs_post_body')


def craw_handler(text,content_id,title_id):
	selector = etree.HTML(text)
	content = selector.xpath(content_id)
	if len(content) > 1:
		raise ValueError('content_id is not unique, please check')
	elif len(content) == 0:
		raise ValueError('page is empty, please check the content_id you use')
	else:
		final_content=etree.tostring(content[0], pretty_print=True,encoding='unicode')

	title = selector.xpath(title_id)
	if len(title) > 1:
		raise ValueError('title_id is not unique, please check')
	elif len(title) == 0:
		raise ValueError('title is empty, please check the title_id you use')
	else:
		final_title=title[0].xpath('string(.)')
	return final_content,final_title

# strengthen craw with xpath
def craw_func_main(url,content_id,title_id):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    logging.info("start parse info from {}".format(url))
    try:
        res = requests.get(url,headers=headers,timeout=200)
    except:
    	raise ValueError('page error')
    if res.status_code == 200:
    	logging.info("start get interested content")
    	final_content,final_title=craw_handler(res.text,content_id,title_id)
    	# selector = etree.HTML(res.text)
    	# content = selector.xpath(content_id)
    	# if len(content) > 1:
    	# 	raise ValueError('content_id is not unique, please check')
    	# elif len(content) == 0:
    	# 	raise ValueError('page is empty, please check the content_id you use')
    	# else:
    	# 	final_content=etree.tostring(content[0], pretty_print=True,encoding='unicode')

    	# title = selector.xpath(title_id)
    	# if len(title) > 1:
    	# 	raise ValueError('title_id is not unique, please check')
    	# elif len(title) == 0:
    	# 	raise ValueError('title is empty, please check the title_id you use')
    	# else:
    	# 	final_title=title[0].xpath('string(.)')
    return final_content,final_title

def convert_to_markdown(content):
    import html2text
    logging.info("convert HTML to arkdown with method {}".format("html2text"))
    # use html2text
    h = html2text.HTML2Text()
    # in case link with \n
    h.body_width = 0
    # todo: does not work 
    h.images_as_html=True
    # start to convert to markdown
    logging.info("start to convert to markdown")
    markdown_content=h.handle(content)
    return markdown_content

def write_to_markdown(out_path,out_file,content,title):
    out_file_path=out_path + '/' + out_file if out_file else out_path + '/' + title + '.md'
    # is path exists
    isExists=os.path.exists(out_path)
    if not isExists:
        logging.info("create dir with path {}".format(out_path))
        os.makedirs(out_path) 
    logging.info("write markdown to {}".format(out_file_path))
    #  notice the encoding type
    with open(out_file_path,'w',encoding='utf-8') as out:
        out.write(content)