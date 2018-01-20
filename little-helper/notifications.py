# Notifications Manager
import json
import time
from random import randint
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from util.like_util import get_links, like_image, update_user_data, update_user_data_timestamp
import pdb 


class Notifications(object): 

	def __init__(self, browser, username, sleep_interval_lower=10, sleep_interval_upper=20): 
		self.load_notification_data()
		self.load_engagement_data()
		self.load_user_data()
		self.sleep_interval_lower = sleep_interval_lower
		self.sleep_interval_upper = sleep_interval_upper 
		self.browser = browser
		self.username = username
	 	# self.timer()

	def timer(self): 
	 	while True: 
			self.notifications()
			self.save_data()
			self.sleep()

	def notifications(self):		
		all_notifications = self.get_notifications()
		self.parse_notifications(all_notifications)				
		self.act_on_notifications()

	def act_on_notifications(self):
		# users = self.notification_tracking.keys()
		sorted_users = sorted(self.user_data.items(), key=lambda y: (y[1]['last_notification']), reverse=True)
		print('Managing relations with {} users'.format(len(sorted_users)))
		time.sleep(2)
		number_engaged = 0 
		for entry in sorted_users:
			user = entry[0]
			should_engage = self.should_engage(user)			
			if should_engage[0]:
				print("Engaging with: {}".format(user))
				try:
					update_user_data(self.browser, user, self.user_data)
					links = get_links(self.browser, user, randint(3, 5), True, type_flag='user')
				except NoSuchElementException:
					print('Element not found, skipping this username')
					continue 
				if links: # if the user is private this will be false 
					number_engaged += 1
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
			else:
				# print("Not engaging with: {} because {}".format(user, should_engage[1]))
				pass
		print("Engaged with {} out of {}".format(number_engaged, len(sorted_users)))

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

		if user in self.user_data.keys():
			if self.user_data[user]['black_list'] ==  True:
				return (False, 'this user is black_listed')

		if user in self.engaged_already.keys(): 
			users_engagment = self.engaged_already[user]
		else: 
			return (True, 'this user has not been engaged with yet')
		users_notifications.sort(key=lambda tup: tup[1])
		users_engagment.sort(key=lambda tup: tup[1])
		summary = self.relationship_summary(users_engagment, users_notifications)
		# Rule check 
		# result =  users_engagment[-1][-1] < users_notifications[-1][-1]
		result = summary[-1][0] == 'notification'
		if result: 
			# pdb.set_trace()
			return (True, 'this user has engaged with you since your last engagment')
		else:
			return (False, 'this user has not engaged with you since your last engagment')

	def get_notifications(self):
		try:
			self.browser.get('https://www.instagram.com/' + self.username)
			button = self.browser.find_element_by_xpath("//nav/div[2]/div/div/div[3]/div/div[2]")
		except NoSuchElementException:
			raise RuntimeWarning('There are no notifications')
		button.click()
		all_notifications = self.browser.find_elements_by_class_name('_75ljm')
		return all_notifications

	def parse_notifications(self, notifications):
		for i in range(len(notifications)):
			notification = notifications[i]
			username = notification.find_element_by_class_name('_2g7d5').text
			raw_action = notification.find_element_by_class_name('_b96u5').text
			if 'like' in raw_action:
				action = 'like'
			elif 'comment' in raw_action:
				action = 'comment'
			elif 'follow' in raw_action:
				action = 'follow'
			raw_time = notification.find_element_by_class_name('_3lema').get_attribute('datetime')
			time = raw_time.split('T')[0] + ' ' + raw_time.split('T')[1][:-1]
			if username and action and time:
				if self.add_action(time, username, action):
					update_user_data_timestamp(username, self.user_data)

	def add_action(self, time, liker_name, notification_type):
		''' update notification tracking
			return true if the user object is updated, false otherwise
		'''
		action = [notification_type, time]
		got_added = True
		if liker_name in self.notification_tracking.keys():
			if action not in self.notification_tracking[liker_name]:
				self.notification_tracking[liker_name].append((notification_type, time))
				print('Adding action for existing user: {} {}'.format(liker_name, action))
			else: 
				got_added = False
		else: 
			self.notification_tracking[liker_name] = [action]
			print('Adding user: {} with action {}'.format(liker_name, action))
		return got_added

	def relationship_summary(self, engagments, notifications):
		""" x_notifications = [ [u'following', u'2017-12-19 12:28:16'], [u'following', u'2017-12-22 12:28:16'], [u'following', u'2017-12-18 12:28:16']]
			x_engagments = [[u'liked', u'2017-12-20 09:05:19']]
			Results in [['notification', 2], ['engagment', 1], ['notification', 1]]
			The purpose of this function is to show the summary of the combined interactions
		"""
		engagments.sort(key=lambda list:list[1])
		engagments = [['engagment', e] for e in engagments]
		notifications.sort(key=lambda list:list[1])
		notifications = [['notification', n] for n in notifications]
		flattened = engagments + notifications
		flattened.sort(key=lambda list: list[1][1])
		summary = []
		for i in range(len(flattened)): 
			element = flattened[i]
			if len(summary) == 0: 
				entry = [element[0], 1]
				summary.append(entry)
			else:
				if element[0] == summary[-1][0]:
					summary[-1][1] = summary[-1][1] + 1
				else:
					entry = [element[0], 1]
					summary.append(entry)
		return summary

	def sleep(self):
		sleep_time_minutes = randint(self.sleep_interval_lower, self.sleep_interval_upper)
		# sleep_time_minutes = randint(2, 5)
		print('Sleeping for {} starting at {}'.format(sleep_time_minutes, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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

	def save_data(self): 
		self.save_notification_data()
		self.save_engagement_data()
		self.save_user_data()

	def save_notification_data(self): 
		try: 
			json.dump(self.notification_tracking, open('../data/notification_tracking.txt', 'w'))
			print("notification_tracking file saved")
		except(Exception) as e:
			print("Exception saving notification_tracking: {}".format(e)) 

	def save_engagement_data(self): 
		try: 
			json.dump(self.engaged_already, open('../data/engaged_already.txt', 'w'))
			print("engaged_already file saved")
		except(Exception) as e:
			print("Exception saving engaged_already: {}".format(e)) 

	def save_user_data(self): 
		try: 
			json.dump(self.user_data, open('../data/user_data.txt', 'w'))
			print("user_data file saved")
		except(Exception) as e:
			print("Exception saving user_data: {}".format(e)) 
