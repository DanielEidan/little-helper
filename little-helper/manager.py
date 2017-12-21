# Manager class 
from browser import Browser
from notifications import Notifications
from commenter import Commenter
from util.login_util import login_user


""" This class will initiate the helpers and run the main 
	execution thread of the program. 
"""
class Manager(object): 
	
	def __init__(self, username, password):
		self.logFile = open('../logs/logFile.txt', 'a')
		browser = Browser()
		self.browser = browser.get_browser()
		self.username = username 
		self.password = password
		self.login()

	def login(self): 
		logged_in = login_user(self.browser,self.username, self.password)
		if logged_in: 
			print('Logged in successfully!')
			self.logFile.write('Logged in successfully!\n')
		else:
			print('Login failed!')
			self.logFile.write('Login failed!\n')

	def notification_manager(self):
		self.notification_manager = Notifications(self.browser, self.username)

	def commenter(self): 
		self.commenter = Commenter(self.browser)		
		tags = ['makeportraits','thecreatorclass','snobshots','creativevagrants']
		self.commenter.comment_by_tag(tags, 2)


if __name__ == '__main__': 

	# These will be removed. 
	username = ''
	password = ''

	# Log in with the manager 
	session = Manager(username, password)

	# Run the notification module 
	session.notification_manager() 

	# Run the Commeter
	# session.commenter()
