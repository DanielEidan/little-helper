# follower.py

from browser import Browser
from util.like_util import get_links, like_image, update_user_data, update_user_data_timestamp
import pdb 



class Follower(object): 

	def __init__(self, browser, username): 
		self.browser = browser
		self.username = username


	def get_followers(self, account): 
		''' Return the account names of the followers of the account named account. 
		''' 
		pdb.set_trace()
		return []
	
	def get_following(self, account): 
		''' Return the account names of all the accounts that the account named 
			account is following.
		'''
		pdb.set_trace()
		return []
