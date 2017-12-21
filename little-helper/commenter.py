# -*- coding: utf-8 -*-
# commenter 

from selenium.common.exceptions import NoSuchElementException
from util.like_util import get_links, like_image, update_user_data
from util.clarifai_util import check_image
import time

import pdb

class Commenter(object):

	def __init__(self, browser, media=None, skip_top=True):
		self.browser = browser			
		

	def comment_by_tag(self, tags, amount):
		
		commented = 0
		tags = list(map(str.strip, tags))
		for index, tag in enumerate(tags, 1):
			print('Tag [{}/{} - {}]'.format(index, len(tags), tag.encode('utf-8')))
			try: 
				links = get_links(self.browser, amount=amount, tag=tag.encode('utf-8'), type_flag='tag')
				for i, link in enumerate(links, 1):
					print('Tag [{}/{} - {}]'.format(i, amount, tag.encode('utf-8')))	
					self.browser.get(link)
					success, attributes = check_image(self.browser)
					if success:
						self.comment(attributes)
			except NoSuchElementException:
				print('Cant get images for tag [{}/{} - {}]'.format(index, len(tags), tag.encode('utf-8')))
				continue
			

	def comment(self, attributes): 
		comment_text = self.get_comment_text(attributes)
		time.sleep(2)
		self.open_comment_section()
		time.sleep(2)
		comment_input = self.get_comment_input()
		time.sleep(2)
		if len(comment_input): 
			comment_input[0].clear()
			time.sleep(2)
			self.browser.execute_script("arguments[0].value = '" + comment_text + " ';", comment_input[0])
			time.sleep(2)
			comment_input[0].send_keys("\b")
			time.sleep(2)	
			comment_input = self.get_comment_input()
			time.sleep(2)
			comment_input[0].submit()
		else:
			print('Warning: Comment Action Likely Failed: Comment Element not found')

		print("Commented: {}".format(comment_text.encode('utf-8')))
		pdb.set_trace()
		time.sleep(2)

	def get_comment_text(self, attributes):
		# 'people', 'man', 'portriat'
		# 'people', 'man', 'fashion'
		# 'people', 'man', 'model'
		# 'people', 'girl', 'portriat'
		# 'people', 'woman', 'portriat'
		# 'people', 'girl', 'fashion'
		# 'people', 'woman', 'fashion'
		# 'people', 'girl', 'model'
		# 'people', 'woman', 'model'
		# 'people', 'child'
		# 'no people', 'footwear'
		# 'no people', 'foot'
		# 'no people', 'shoe'
		# 'no people', 'street'
		# 'no people', 'city'
		# 'no people', 'travel', 'outdoors'
		# 'no people', 'travel', 'sky'
		# 'no people', 'travel', 'landscape'
		# 'no people', 'travel', 'water'
		return "Amazing shot!"


	def open_comment_section(self):
		missing_comment_elem_warning = (
			'--> Warning: Comment Button Not Found:'
			' May cause issues with browser windows of smaller widths')
		comment_elem = self.browser.find_elements_by_xpath("//a[@role='button']/span[text()='Comment']/..")
		if len(comment_elem) > 0:
			try:
				self.browser.execute_script("arguments[0].click();", comment_elem[0])
			except WebDriverException:
				print(missing_comment_elem_warning)
		else:
			print(missing_comment_elem_warning)


	def get_comment_input(self):
		comment_input = self.browser.find_elements_by_xpath('//textarea[@placeholder = "Add a comment…"]')
		if len(comment_input) <= 0:
			comment_input = self.browser.find_elements_by_xpath('//input[@placeholder = "Add a comment…"]')
		return comment_input


