import os
import re 
from bs4 import BeautifulSoup

def read_local_html(local_file):
	pat=re.compile(r'.*/(.*)\.html')
	title=re.search(pat,local_file).group(1)
	with open(local_file,'r',encoding='utf-8') as evernote:
		# evernote_info=evernote.readlines()
		# fi_evernote=''.join(evernote_info)
		# # print (evernote_info)
		# markdown_content=convert_to_markdown(fi_evernote)
		# # print (markdown_content)
		# write_to_markdown('.','',markdown_content,'title')
		Soup = BeautifulSoup(evernote,'html.parser')
		content = Soup.select("body")
		if len(content) == 0:
			raise ValueError('page is empty, please check the content_id you use')
		else:
			final_content=content[0]
	return str(final_content),title

def sub_image_link(content,cloud_image_base):

	pat=re.compile(r'src="(.*?)/(.*?\..*?")')
	final_content=re.sub(pat,'src="{}/\\2'.format(cloud_image_base),content)

	return final_content
def replace_space(content):
	pat=re.compile(r'src=".*?/(.*?\..*?")')
	pic_li=re.findall(pat,content)
	for i in pic_li:
		after_i="%20".join(i.split())
		# print (str(after_i))
		content=content.replace(i,after_i)
	return content

if __name__ == '__main__':
	file_path='C:/Users/14910/Desktop/VS code配置.html'
	final_content,title=read_local_html(file_path)
	cloud_image_base='https://showteeth.oss-cn-beijing.aliyuncs.com/blog_img/VS_code配置'
	sub_content=sub_image_link(final_content,cloud_image_base)
	space_content=replace_space(sub_content)
	print (space_content)