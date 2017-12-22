# -*- coding: utf-8 -*-
# commenter 

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from util.like_util import get_links, like_image, update_user_data
from util.clarifai_util import check_image
import time
import emoji
import random
import pdb


class Commenter(object):

	def __init__(self, browser, username, media=None, skip_top=True):
		self.browser = browser
		self.username = username
		
	def comment_by_tag(self, tags, amount):		
		commented = 0
		tags = list(map(str.strip, tags))
		for index, tag in enumerate(tags, 1):
			print('Tag [{}/{} - {}]'.format(index, len(tags), tag.encode('utf-8')))
			try: 
				links = get_links(self.browser, amount=amount, tag=tag.encode('utf-8'), type_flag='tag')
				for i, link in enumerate(links, 1):
					print('Tag [{}/{} - tag:{} link:{}]'.format(i, amount, tag.encode('utf-8'), link))					
					self.browser.get(link)
					success, attributes = check_image(self.browser)
					if success:
						self.comment(attributes)
			except NoSuchElementException:
				print('Cant get images for tag [{}/{} - {}]'.format(index, len(tags), tag.encode('utf-8')))
				continue
			
	def comment(self, attributes): 
		commented_already = self.did_comment_already()
		if not commented_already:
			comment_text = self.get_comment_text(attributes)
			time.sleep(2)
			self.open_comment_section()
			time.sleep(2)
			comment_input = self.get_comment_input()
			time.sleep(2)
			if len(comment_input):
				try: 
					comment_input[0].clear()
					time.sleep(2)
					self.browser.execute_script("arguments[0].value = '" + comment_text + " ';", comment_input[0])
					time.sleep(2)
					comment_input[0].send_keys("\b")
					time.sleep(2)	
					comment_input = self.get_comment_input()
					time.sleep(2)
					comment_input[0].submit()
				except StaleElementReferenceException as e: 
					print('Exception on comment: {}'.format(e))
			else:
				print('Warning: Comment Action Likely Failed: Comment Element not found')
			print("Commented: {} \n For tags: {}".format(comment_text.encode('utf-8'), attributes))
			time.sleep(2)
		else: 
			print("Attempted to comment on a previously commented media. -------------------- ")
			time.sleep(2)

	def did_comment_already(self):
		# Note: if there are more comments than visible in the browser this function does not load them all. 
		# 		therfore there is a chance that this will return a false negative. 
		all_comments = self.browser.find_element_by_class_name('_4a48i')
		return self.username in all_comments.text

	def get_comment_text(self, attributes):
		comment = '' 
		if ('people' or 'person')in attributes:
			if 'man' in attributes:
				if 'portrait' in attributes: 
					comment = random.choice(['beautiful portrait', 'nice portrait', 'intimate portrait'])
				elif 'fashion' in attributes: 
					comment = random.choice(['great look', 'love the fit', 'stylish', 'great fit', 'sharp look', 'fashion goals'])
				elif 'model' in attributes: 
					comment = random.choice(['looking good', 'beautiful', 'great look', 'goals'])
				else: 
					comment = random.choice(['good stuff man', 'looking good man'])

			elif ('woman' or 'girl') in attributes:
				if 'portrait' in attributes: 
					comment = random.choice(['beautiful portrait', 'nice portrait', 'intimate portrait', 'stunning portrait', 'intimate and beautiful', 'beautiful and intimate'])
				elif 'fashion' in attributes: 
					comment = random.choice(['great look babe', 'love the fit', 'so stylish', 'wow, what a great fit', 'sharp look', 'fashion goals', 'sexy outfit'])
				elif 'model' in attributes: 
					comment = random.choice(['babe', "you're stunning", 'stunning', 'gorgeous', 'wow, so beautiful'])
				else: 
					comment = random.choice(['good stuff girl', 'looking great girl'])

			elif 'child' in attributes: 
				comment = random.choice(['so cute', 'adorable', 'precious'])
			else: 
				comment = random.choice(['looking good'])
		elif 'no person' in attributes:
			if 'footwear' or 'foot' or 'shoe' in attributes:
				comment = random.choice(['nice kick', 'dope cop', 'kicks on fire', 'fire kicks', 'save me a pair'])
			elif ('street' or 'city') in attributes:
				comment = random.choice(['urban vibes', 'street style', 'urban grind', 'urban streets'])
			elif 'travel' in attributes: 
				comment = random.choice(['wanderlust', 'destination goals', 'I want to be there!'])
			elif 'sky' in attributes:
				comment = random.choice(['beautiful sky', 'that sky view though'])
			elif 'water' in attributes:
				comment = random.choice(['that water', 'I want to jump right in'])
			elif 'landscape' or 'outdoors' in attributes:
				comment = random.choice(['that view', 'view goals', 'keep exploriong', 'look at that view'])
		else: 
			comment = random.choice(['good stuff', 'nice', 'beautiful', 'amazing', 'dope', 'great stuff', 'love it!' ])
		emoji_icon = random.choice([':smile:', ':laughing:', ':blush:', ':smiley:', ':relaxed:', ':kissing_closed_eyes:', ':flushed:', ':relieved:', ':satisfied:', ':grin:', ':wink:', ':stuck_out_tongue_winking_eye:', ':stuck_out_tongue_closed_eyes:', ':grinning:', ':kissing:', ':kissing_smiling_eyes:', ':stuck_out_tongue:', ':sunglasses:', ':fire:', ':thumbsup:', ':ok_hand:', ':wave:', ':raised_hands:', ':pray:', ':clap:', ':100:', ':heavy_check_mark:', ':bangbang:', ':heavy_exclamation_mark:'])
		comment = emoji.emojize('{}{}'.format(comment, emoji_icon), use_aliases=True)
		return comment 


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
