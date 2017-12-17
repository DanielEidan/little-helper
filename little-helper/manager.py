# Manager class 
from browser import Browser
from notifications import Notifications
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


if __name__ == '__main__': 

	username = 'with.eden'
	password = '438queenwest'

	session = Manager(username, password)
	session.notification_manager()
