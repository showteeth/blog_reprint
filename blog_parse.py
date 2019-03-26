import os
import argparse
import logging
logging.basicConfig(level=logging.DEBUG,format="%(levelname)s-%(filename)s:[%(lineno)d]-%(message)s")
from craw_func import craw_func_main,convert_to_markdown,write_to_markdown
from process_evernote_html import read_local_html,sub_image_link,replace_space

def blogs(args):
	if args.blog_name == "cnblogs":
		logging.info("start parse page from {}".format(args.blog_name))
		content_id='//*[@id="cnblogs_post_body"]'
		title_id='//*[@id="cb_post_title_url"]'

	elif args.blog_name == "csdn":
		logging.info("start parse page from {}".format(args.blog_name))
		content_id='//*[@id="article_content"]'
		title_id='//*[@id="mainBox"]/main/div[1]/div/div/div[1]/h1'
	elif args.blog_name == "jianshu":
		logging.info("start parse page from {}".format(args.blog_name))
		content_id='/html/body/div[1]/div[2]/div[1]/div[2]/div'
		title_id='/html/body/div[1]/div[2]/div[1]/h1'
	else:
		logging.info("start parse page from others blogs")
		content_id=args.content_id
		title_id=args.title_id
	return content_id,title_id

def main():
	# paras 
	parser = argparse.ArgumentParser(description='reprint blog with markdown')
	common_group=parser.add_argument_group('common parameters in common blogs')

	common_group.add_argument('-b' , '--blog_name' , type=str ,
						help='which blog the url is from(default cnblogs)',default="cnblogs",
						choices=['cnblogs','csdn','evernote','jianshu','others'])
	common_group.add_argument('-p' , '--out_path' , type=str ,
						help='path to save markdown file( default current folder)',default=".")
	common_group.add_argument('-o' , '--out_file' , type=str ,
						help='file to save markdown')	


	blog_group=parser.add_argument_group('blog(other than evernote) specific parameters')
	blog_group.add_argument('-u' , '--url' , type=str,
						help='url to parse')
	blog_group.add_argument('-c' , '--content_id' , type=str ,
						help='xpath of content body')
	blog_group.add_argument('-t' , '--title_id' , type=str ,
						help='xpath of title')
	# parser.add_argument('-m' , '--method' , type=str ,
	# 					help='method to trans html to markdown',default="html2text"
	# 					,choices=['html2text','tomd'])
	evernote_group=parser.add_argument_group('evernote specific parameters')
	evernote_group.add_argument('-l' , '--local_html' , type=str ,
						help='full path of local evernote export html')
	evernote_group.add_argument('-i' , '--clout_image_base' , type=str ,
						help='aliyun image link base',default='https://showteeth.oss-cn-beijing.aliyuncs.com/blog_img')
	evernote_group.add_argument('-f' , '--clout_image_folder' , type=str ,
						help='aliyun image link folder')
	args = parser.parse_args()

	if args.blog_name != "evernote":
		logging.info("============step1: get blog congtent and title id==========")
		content_id,title_id=blogs(args)
		
		logging.info("============step2: get content and title==========")
		final_content,final_title=craw_func_main(args.url,content_id,title_id)

		logging.info("============step3: convert to markdown==========")
		markdown_content=convert_to_markdown(final_content)

		logging.info("============step4: write to file==========")
		write_to_markdown(args.out_path,args.out_file,markdown_content,final_title)
	else:
		logging.info("============start process evernote html file==========")
		logging.info("============step1: process local html==========")
		content,title=read_local_html(args.local_html)
		logging.info("============step2: sub image links==========")
		cloud_image_link=args.clout_image_base + '/' + args.clout_image_folder \
			if args.clout_image_folder else args.clout_image_base
		final_content=sub_image_link(content,cloud_image_link)
		logging.info("============step3: replace link space==========")
		space_content=replace_space(final_content)
		logging.info("============step4: convert to markdown==========")
		markdown_content=convert_to_markdown(space_content)
		logging.info("============step5: write to file==========")
		write_to_markdown(args.out_path,args.out_file,markdown_content,title)


if __name__ == '__main__':
	main()
