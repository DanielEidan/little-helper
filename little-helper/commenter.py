# -*- coding: utf-8 -*-
# commenter 

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from util.like_util import get_links, like_image, update_user_data
from util.clarifai_util import check_image, collect_image_data
from random import randint
import time
import emoji
import random
import pdb


class Commenter(object):

	def __init__(self, browser, username, media=None, skip_top=True):
		self.browser = browser
		self.username = username
		
	def comment_by_tag(self, tags, amount, engage_user=False):		
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
						if engage_user:
							self.browser.find_element_by_class_name('_2g7d5').click()							
							username = self.browser.current_url.split('/')[-2] 
							self.engage_with_user(username)						
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

					# like the image you just commented on
					like_image(self.browser)
				except (StaleElementReferenceException, WebDriverException) as e: 
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
		comment = random.choice(['nice', 'beautiful', 'cool', 'great shot', 'love it', 'nice work'])
		# generic attributes
		if ('fashion' or 'model') in attributes: 			
			if ('woman' or 'girl') in attributes:
				comment = random.choice(['babe', "you're stunning", 'stunning', 'gorgeous', 'wow, so beautiful', 'great look babe', 'love the fit', 'so stylish', 'wow, what a great fit', 'sharp look', 'fashion goals', 'great outfit'])
			elif 'man' in attributes: 
				comment = random.choice(['great look', 'love the fit', 'stylish', 'great fit', 'sharp look', 'fashion goals', 'looking good', 'beautiful', 'great look', 'goals'])
		if 'portrait' in attributes:
			if ('woman' or 'girl') in attributes:
				comment = random.choice(['beautiful portrait', 'nice portrait', 'intimate portrait', 'stunning portrait', 'intimate and beautiful', 'beautiful and intimate'])
			elif 'man' in attributes: 
				comment = random.choice(['beautiful portrait', 'nice portrait', 'portrait on point'])

		# specific attributes, that will override generic ones
		if 'monochrome' in attributes:
			comment = random.choice(['love the black and white'])
		if ('vehicle' or 'car' or 'transportation system') in attributes:
			comment = random.choice(['nice ride', 'nice whip', 'dope ride', 'nice wheels'])
		if ('building' or 'architecture') in attributes:
			comment = random.choice(['beautiful architecture', 'nice lines', 'nice building', 'great lines'])
		if ('winter' or 'snow') in attributes: 
			comment = random.choice(['winter magic', 'beautiful snow', 'winter wonderland'])
		if ('winter' or 'snow') in attributes: 
			comment = random.choice(['snow', 'snow white', 'love the winter vibes'])
		if ('sneakers' or 'foot' or 'shoe' or 'footwear') in attributes:
			comment = random.choice(['nice kick', 'dope cop', 'kicks on fire', 'fire kicks', 'save me a pair'])
		if ('sexy' or 'nude') in attributes:
			comment = random.choice(['so sexy', 'sexy', 'damn', 'hot', 'omg, wow', 'sexy look'])
		if ('child') in attributes:
			comment = random.choice(['so cute', 'adorable', 'precious', 'awwww...'])
		if ('street' or 'city') in attributes:
			comment = random.choice(['urban vibes', 'street style', 'urban grind', 'urban streets'])
		if 'travel' in attributes: 
			comment = random.choice(['wanderlust', 'destination goals', 'I want to be there!'])
		if 'sky' in attributes:
			comment = random.choice(['beautiful sky', 'that sky view though'])
		if 'water' in attributes:
			comment = random.choice(['that water', 'I want to jump right in', 'love the water', 'beautiful water'])
		if ('landscape' or 'outdoors' or 'adventure' or 'travel', 'nature') in attributes:
			comment = random.choice(['that view', 'view goals', 'keep exploring', 'look at that view'])
		if ('watch' or 'clock') in attributes: 
			comment = random.choice(['nice piece', 'keep that time'])			
		if ('aerial') in attributes: 
			comment = random.choice(['flying high', 'great perspective'])		
		if ('food') in attributes: 
			comment = random.choice(['delicious', 'yum', 'looks delicious'])

		emoji_icon = random.choice([':smile:', ':laughing:', ':blush:', ':smiley:', ':relaxed:', ':kissing_closed_eyes:', ':flushed:', ':relieved:', ':satisfied:', ':grin:', ':wink:', ':stuck_out_tongue_winking_eye:', ':stuck_out_tongue_closed_eyes:', ':grinning:', ':kissing:', ':kissing_smiling_eyes:', ':stuck_out_tongue:', ':sunglasses:', ':fire:', ':thumbsup:', ':ok_hand:', ':wave:', ':raised_hands:', ':pray:', ':clap:', ':100:', ':heavy_check_mark:', ':bangbang:', ':heavy_exclamation_mark:'])
		comment = emoji.emojize('{}{}'.format(comment, emoji_icon), use_aliases=True)
		return comment


	def engage_with_user(self, user): 
		try:					
			links = get_links(self.browser, user, randint(2, 4), True, type_flag='user')
		except NoSuchElementException:
			print('Element not found, skipping {}'.fomat(user))
		if links: # if the user is private this will be false 
			for link in links:
				print("liking: {}".format(link))
				self.browser.get(link)
				liked = like_image(self.browser)
		else: 		
			print("Not engaging with: {} because they are private".format(user))


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

	def make_clarifai_lable_file(self, tags, amount, engage_user=False):
		commented = 0
		tags = list(map(str.strip, tags))
		for index, tag in enumerate(tags, 1):
			print('Tag [{}/{} - {}]'.format(index, len(tags), tag.encode('utf-8')))
			try: 
				links = get_links(self.browser, amount=amount, tag=tag.encode('utf-8'), type_flag='tag')
				for i, link in enumerate(links, 1):
					print('Tag [{}/{} - tag:{} link:{}]'.format(i, amount, tag.encode('utf-8'), link))					
					self.browser.get(link)
					success, attributes = collect_image_data(self.browser)
					# if success:
					# 	self.comment(attributes)
					# 	if engage_user:
					# 		self.browser.find_element_by_class_name('_2g7d5').click()							
					# 		username = self.browser.current_url.split('/')[-2] 
					# 		self.engage_with_user(username)						
			except NoSuchElementException:
				print('Cant get images for tag [{}/{} - {}]'.format(index, len(tags), tag.encode('utf-8')))
				continue
			
