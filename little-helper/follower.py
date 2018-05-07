# follower.py

import pdb 
import json
import random 	
from browser import Browser
from datetime import datetime, timedelta
from util.time_util import sleep
from util.like_util import get_links, like_image, update_user_data, update_user_data_timestamp, update_user_data_following_them_status, update_user_data_following_me_status
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from notifications import Notifications




class Follower(object): 

	def __init__(self, browser, username): 
		self.browser = browser
		self.username = username
		self.load_user_data()
		self.load_engagement_data()



	def update_followers(self):
		''' Update user data on who's following me. 
		''' 			
		self.browser.get('https://www.instagram.com/' + self.username)
		x = self.browser.find_elements_by_xpath("//main/article/header")
		x[0].find_elements_by_tag_name('li')[1].click() # these are the people that are following my account 
		sleep(2)
		y = self.browser.find_element_by_class_name('_gs38e')
		z1 = y.find_elements_by_tag_name('li')		
		z2 = []
		i = 1
		# while len(z1) != len(z2):
		while len(z1) < 2000:
			i += 1
			print(i)
			z1 = z2
			self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", y)
			sleep(random.randint(1, i/2))
			z2 = y.find_elements_by_tag_name('li')

		z3 = map(lambda i: i.text.split('\n'), z2) # parse into [account_name, user_name, Following/Follow]		
		z4 = map(lambda i: (i[0].encode('utf-8'), i[-1].encode('utf-8')), z3)
		z5 = map(lambda i: (i[0], i[-1] == "Following"), z4) 		
		for i in z5:			
			update_user_data_following_them_status(i[0], i[-1], self.user_data)
			update_user_data_following_me_status(i[0], True, self.user_data)

		self.report()
		self.save_user_data()

	def update_following(self): 
		self.browser.get('https://www.instagram.com/' + self.username)
		x = self.browser.find_elements_by_xpath("//main/article/header")
		x[0].find_elements_by_tag_name('li')[2].click() # these are the people that I follow 
		sleep(2)
		y = self.browser.find_element_by_class_name('_gs38e')
		z1 = y.find_elements_by_tag_name('li')		
		z2 = []
		i = 1		
		# while len(z1) != len(z2):
		while len(z1) < 980:
			i += 1
			print(i)
			z1 = z2
			self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", y)
			sleep(random.randint(1, i/2))
			z2 = y.find_elements_by_tag_name('li')

		z3 = map(lambda i: i.text.split('\n'), z2) # parse into [account_name, user_name, Following/Follow]					
		for i in z3:			
			update_user_data_following_them_status(i[0], True, self.user_data)

		self.report()
		self.save_user_data()

	def report(self):
		num_following = 0
		num_followers = 0
		for key in self.user_data.keys():
			if (("following_me" in self.user_data[key]) and self.user_data[key]["following_me"]):
				num_followers += 1
			if (("following_them" in self.user_data[key]) and self.user_data[key]["following_them"]):
				num_following += 1
		print("Followers: {}, Following: {}".format(num_followers, num_following))

	def load_user_data(self):
		try: 
			user_data = json.load(open('../data/user_data.txt'))
			print("user_data file Loaded")
		except(ValueError, IOError) as e:
			print("Exception on load: {}".format(e))
			print("user_data files initiated")
			user_data = {}
		self.user_data = user_data

	def save_user_data(self):
		try: 
			json.dump(self.user_data, open('../data/user_data.txt', 'w'))
			print("user_data file saved")
		except(Exception) as e:
			print("Exception saving user_data: {}".format(e))

	def load_engagement_data(self): 
		try: 
			engaged_already = json.load(open('../data/engaged_already.txt'))
			print("engaged_already file Loaded")
		except(ValueError, IOError) as e:
			print("Exception on load: {}".format(e))
			print("engaged_already files initiated")
			engaged_already = {}
		self.engaged_already = engaged_already

	def save_engagement_data(self): 
		try: 
			json.dump(self.engaged_already, open('../data/engaged_already.txt', 'w'))
			print("engaged_already file saved")
		except(Exception) as e:
			print("Exception saving engaged_already: {}".format(e)) 

	def engage_with_followers_followers(self, n=5, m=5, amount=5):
		""" Get all my followers 
			Pick a random amount of n followers
				For each follower pick a random amount of m followers
			like a random amount, amount of there pictures
		"""
		followers = []
		for key in self.user_data.keys():
			if (("following_me" in self.user_data[key]) and self.user_data[key]["following_me"]):
				followers.append(key)
		n_followers = random.sample(followers, n)
		for follower in n_followers:
			# pdb.set_trace()
			print("Looking for followers of follower: {}".format(follower))
			self.browser.get('https://www.instagram.com/' + follower)
			try:
				x = self.browser.find_elements_by_xpath("//main/article/header")
				x[0].find_elements_by_tag_name('li')[1].click() # these are the people that are following my account 
				sleep(2)
				y = self.browser.find_element_by_class_name('_gs38e')
			except (NoSuchElementException, IndexError) as e:
				print('Element not found, skipping this username')
				continue 
			z1 = y.find_elements_by_tag_name('li')		
			z2 = []
			i = 1
			while len(z1) < (m * 10) or i < 10:
				i += 1
				z1 = z2
				self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", y)
				sleep(random.randint(1, i/2))
				z2 = y.find_elements_by_tag_name('li')
			z3 = map(lambda i: i.text.split('\n'), z2) # parse into [account_name, user_name, Following/Follow]		
			z4 = map(lambda i: (i[0].encode('utf-8'), i[-1].encode('utf-8')), z3)
			z5 = map(lambda i: (i[0], i[-1] == "Following"), z4)
			m_follower_of_followers = random.sample(z5, m)
			for follower_of_follower in m_follower_of_followers:
				if not self.following_me(follower_of_follower):
					self.engage(follower_of_follower[0], amount)
				else: 
					print("passing on engagment becuase user is already a follower: {}".format(follower_of_follower))
		self.save_engagement_data()

	def following_me(self, user):
		if user in self.user_data.keys() and self.user_data[user]['following_me']:
			return True
		else:
			return False

	def engage(self, user, x): 
		# pdb.set_trace()
		print("Engaging with: {}".format(user))
		try:
			update_user_data(self.browser, user, self.user_data)			
			links = get_links(self.browser, user, amount=x, is_random=True, type_flag='user')
			if links: # if the user is private this will be false 
				for link in links:
					self.browser.get(link)
					liked = like_image(self.browser)
					print("liking: {}".format(link))
					engagment = ('liked', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
					self.add_engagment(user, engagment)
			else:
				engagment = ('User is private', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
				self.add_engagment(user, engagment)
				# print("Not engaging with: {} because they are private".format(user)) 
		except NoSuchElementException:
			print('Element not found, skipping this username')
		

	def add_engagment(self, user, engagment):
		if user in self.engaged_already.keys():
			self.engaged_already[user].append(engagment)
		else:
			self.engaged_already[user] = [engagment]

	def engage_with_feed(self):
		self.browser.get('https://www.instagram.com/')
		pdb.set_trace()


