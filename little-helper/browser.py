# Browser 
from selenium import webdriver
from datetime import datetime, timedelta
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import pdb

class Browser(object): 
	pass

	def __init__(self, page_delay=25): 
		self.logFile = open('../logs/logFile.txt', 'a')		
		self.page_delay = page_delay
		self.set_selenium_local_session()


	def set_selenium_local_session(self): 
		''' initiate a selenium web session. 
		'''		
		chromedriver_location = '../assets/chromedriver'
		chrome_options = Options()
		chrome_options.add_argument('--dns-prefetch-disable')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--lang=en-US')
		chrome_prefs = {'intl.accept_languages': 'en-US'}
		chrome_options.add_experimental_option('prefs', chrome_prefs)
		if False: # This makes chrome Headless 
			chrome_options.add_argument('--headless')
			# Replaces browser User Agent from "HeadlessChrome".
			user_agent = "Chrome"
			chrome_options.add_argument('user-agent={user_agent}'.format(user_agent=user_agent))
		self.browser = webdriver.Chrome(chromedriver_location, chrome_options=chrome_options)
		self.browser.implicitly_wait(self.page_delay)
		self.logFile.write('Session started - %s\n' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

	def get_browser(self):
		return self.browser
