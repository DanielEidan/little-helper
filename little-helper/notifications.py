# Notifications Manager
import json
import time
from random import randint
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException

from util.like_util import get_links, like_image, update_user_data


class Notifications(object): 

	def __init__(self, browser, username, sleep_interval_lower=25, sleep_interval_upper=35): 
		self.load_notification_data()
		self.load_engagement_data()
		self.load_user_data()
		self.sleep_interval_lower = sleep_interval_lower
		self.sleep_interval_upper = sleep_interval_upper 
		self.browser = browser
		self.username = username
	 	self.timer()

	def timer(self, sleep_interval_lower=25, sleep_interval_upper=35): 
	 	while True: 
			self.notifications()
			self.save_notification_data()
			self.save_engagement_data()
			self.save_user_data()
			self.sleep()

	def notifications(self):
		self.browser.get('https://www.instagram.com/' + self.username)
		all_notifications = self.get_notifications()
		self.parse_notifications(all_notifications)
		self.act_on_notifications()

	def act_on_notifications(self):
		users = self.notification_tracking.keys()
		print('Managing relations with {} users'.format(len(users)))
		for user in users:
			should_engage = self.should_engage(user)
			if should_engage[0]:
				update_user_data(self.browser, user, self.user_data)
				print("Engaging with: {}".format(user))
				try:
					links = get_links(self.browser, user, 4, True, type_flag='user')
				except NoSuchElementException:
					print('Element not found, skipping this username')
				if links: # if the user is private this will be false 
					for link in links:
						print("liking: {}".format(link))
						self.browser.get(link)
						liked = like_image(self.browser)                                                
						engagment = ('liked', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
						self.add_engagment(user, engagment)
				else: 
					engagment = ('User is private', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
					self.add_engagment(user, engagment)
					print("Not engaging with: {} because they are private".format(user))
			else:
				print("Not engaging with: {} because {}".format(user, should_engage[1]))

	def add_engagment(self, user, engagment):
		if user in self.engaged_already.keys():
			self.engaged_already[user].append(engagment)
		else:
			self.engaged_already[user] = [engagment]

	def should_engage(self, user):
		''' Return (True/False, 'reason') tuple based on the rules of engagment if action should be taken.
			Rule: if the user has generated notifications since the account owners last engagment, return True.
		'''
		if user in self.notification_tracking.keys(): 
			users_notifications = self.notification_tracking[user]
		else:
			return (False, 'this user is not in the tracked notifications')

		if user in self.engaged_already.keys(): 
			users_engagment = self.engaged_already[user]
		else: 
			return (True, 'this user has not been engaged with yet')
		# Sort notifications in place based on time 
		users_notifications.sort(key=lambda tup: tup[1])
		users_engagment.sort(key=lambda tup: tup[1])
		# Rule check 
		result =  users_engagment[-1][-1] < users_notifications[-1][-1]
		if result: 
			return (True, 'this user has engaged with you since your last engagment')
		else:
			return (False, 'this user has not engaged with you since your last engagment')

	def get_notifications(self):
		try:
			button = self.browser.find_element_by_xpath("//nav/div[2]/div/div/div[3]/div/div[2]")
		except NoSuchElementException:
			raise RuntimeWarning('There are no notifications')
		button.click()     
		all_notifications = self.browser.find_element_by_xpath("//nav/div[2]/div/div/div[3]/div/div[2]/div/div/div[4]/ul").text
		return all_notifications.split('\n')    	

	def parse_notifications(self, notifications):
		''' Convert time to date format, and update notification tracking'''
		for notification_type in ['liked', 'following']:
			likers_names = [x.split(' ')[0] for x in notifications if notification_type in x]
			likers_times  = [x.split(' ')[-1] for x in notifications if notification_type in x]
			for i in range(len(likers_names)):
				liker_name = likers_names[i]
				liker_time = likers_times[i]
				if liker_time[-1]== 'h':
					hours = int(liker_time[-2].encode('utf-8')) # not sure if I need this encode 
					time = (datetime.now() - timedelta(hours = hours)).strftime('%Y-%m-%d %H:%M:%S')
				else:
					if is_number(liker_time[-3]):
						minutes = liker_time[-3:-1].encode('utf-8')
					else:
						minutes = liker_time[-2].encode('utf-8')
					minutes = int(minutes)
					time = (datetime.now() - timedelta(minutes = minutes)).strftime('%Y-%m-%d %H:%M:%S')
				self.add_action(time, liker_name, notification_type)

	def add_action(self, time, liker_name, notification_type):
		''' update notification tracking'''
		if liker_name in self.notification_tracking.keys():
			self.notification_tracking[liker_name].append((notification_type, time))
		else: 
			self.notification_tracking[liker_name] = [(notification_type, time)]

	def sleep(self):
		sleep_time_minutes = randint(self.sleep_interval_lower, self.sleep_interval_upper)
		print('Sleeping for {}'.format(sleep_time_minutes))
		time.sleep(60 * sleep_time_minutes) 

	def load_notification_data(self): 
		try: 	
			notification_tracking = json.load(open('../data/notification_tracking.txt'))
			print("notification_tracking file loaded")
		except(ValueError, IOError) as e:
			print("Exception on load: {}".format(e))
			print("notification_tracking file initiated")            
			notification_tracking = {}
		self.notification_tracking = notification_tracking

	def load_engagement_data(self): 
		try: 
			engaged_already = json.load(open('../data/engaged_already.txt'))
			print("engaged_already file Loaded")
		except(ValueError, IOError) as e:
			print("Exception on load: {}".format(e))
			print("engaged_already files initiated")
			engaged_already = {}
		self.engaged_already = engaged_already

	def load_user_data(self):
		try: 
			user_data = json.load(open('../data/user_data.txt'))
			print("user_data file Loaded")
		except(ValueError, IOError) as e:
			print("Exception on load: {}".format(e))
			print("user_data files initiated")
			user_data = {}
		self.user_data = user_data

	def save_notification_data(self): 
		try: 
			json.dump(self.notification_tracking, open('../data/notification_tracking.txt', 'w'))
		except(Exception) as e:
			print("Exception saving notification_tracking: {}".format(e)) 

	def save_engagement_data(self): 
		try: 
			json.dump(self.engaged_already, open('../data/engaged_already.txt', 'w'))
		except(Exception) as e:
			print("Exception saving engaged_already: {}".format(e)) 

	def save_user_data(self): 
		try: 
			json.dump(self.user_already, open('../data/user_already.txt', 'w'))
		except(Exception) as e:
			print("Exception saving user_already: {}".format(e)) 

# this should be moved out to a utility tool 
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		pass
	return False 