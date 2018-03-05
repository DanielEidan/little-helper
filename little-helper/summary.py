# summary.py
import json
from datetime import datetime, timedelta

class Summary(object): 
	""" This class will provide summary statistics. 
	"""

	def __init__(self, user_data_file_name, engagment_data_file_name, notification_data_file_name):
		self.user_date = self.load_data(user_data_file_name)
		self.engagment_data = self.load_data(engagment_data_file_name)
		self.notification_data = self.load_data(notification_data_file_name)

	def load_data(self, file_name): 
		try: 	
			data_json = json.load(open('../data/{}'.format(file_name)))
			# print("File loaded")
		except(ValueError, IOError) as e:
			print("Exception on load: {}".format(e))
		return data_json

	def notifications_in_last_x_hours(self, x):
		counter = 0
		for user in self.notification_data.keys(): 
			user_data = self.notification_data[user] 
			for notification in user_data: 
				if notification[-1] > (datetime.utcnow() - timedelta(hours= x)).strftime('%Y-%m-%d %H:%M:%S'):
					print("{} - {}".format(user, notification))
					counter += 1
		return counter
		# (datetime.utcnow() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')

	def specific_notification_in_last_x_hours(self, x, notification_type): 
		likes = {}
		for user in self.notification_data.keys(): 
			user_data = self.notification_data[user]
			for notification in user_data: 
				if (notification[-1] > (datetime.utcnow() - timedelta(hours= x)).strftime('%Y-%m-%d %H:%M:%S')) and (notification[0] == notification_type):
					# print("{} - {}".format(user, notification))
					if user in likes.keys():
						likes[user].append(notification)
					else: 
						likes[user] = [notification]
		return likes

def pretty_print(d): 
	total = 0
	for key in d.keys(): 
		print('user:{} \ntotal:{}'.format(key, len(d[key])))
		# print('user:{} \n total:{} \n details:{}'.format(key, len(d[key]), d[key]))	
		total += len(d[key])
	print('\ntotal:{} \n'.format(total))	

if __name__ == '__main__': 
	summary = Summary('user_data.txt', 'engaged_already.txt', 'notification_tracking.txt')
	# print(summary.notifications_in_last_x_hours(24))
	pretty_print(summary.specific_notification_in_last_x_hours(72, 'like'))
	pretty_print(summary.specific_notification_in_last_x_hours(72, 'comment'))
	pretty_print(summary.specific_notification_in_last_x_hours(72, 'following'))

