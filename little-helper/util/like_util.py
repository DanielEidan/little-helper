# like_util
import random
from math import ceil
from .time_util import sleep
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pdb 
import re 

def like_image(browser):
	""" Like the browser opened image and return True. 
		Otherwise return False 
	"""
	like_elem = browser.find_elements_by_xpath("//a[@role='button']/span[text()='Like']/..")
	liked_elem = browser.find_elements_by_xpath("//a[@role='button']/span[text()='Unlike']")
	liked = False
	if len(like_elem) == 1:
		like_elem[0].send_keys("\n")
		print('--> Image Liked!')
		sleep(2)
		liked = True
	elif len(liked_elem) == 1:
		print('--> Already Liked!')
	else:
		print('--> Invalid Like Element!')
	return liked

def get_links(browser, username=None, amount=3, is_random=False, media=None, skip_top=True, tag=None, type_flag='user'):
	""" Fetches the number of links specified type (type_flag='user'/'tag')
		by amount and returns a list of links
		Raises: NoSuchElementException
	"""
	# pdb.set_trace()
	media = get_media_formats(media)
	if type_flag == 'user':
		print('Attempting to get image list for {}'.format(username))
		browser.get('https://www.instagram.com/' + username)
	elif type_flag == 'tag':
		print('Attempting to get image for TAG {}/'.format(tag))		
		browser.get('https://www.instagram.com/explore/tags/' + (tag[1:] if tag[:1] == '#' else tag))
		sleep(2)
		for i in range(3):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			sleep(2)
	sleep(2)
	body_elem = browser.find_element_by_tag_name('body')
	sleep(2)

	links = []
	try:
		if type_flag == 'tag' and skip_top:
			main_elem = browser.find_element_by_xpath('//main/article/div[2]')
		elif type_flag == 'user':
			main_elem = browser.find_element_by_tag_name('main')
			if is_random:
				browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				sleep(2)
		link_elems = main_elem.find_elements_by_tag_name('a')
		if link_elems:
			links = [link_elem.get_attribute('href') for link_elem in link_elems if link_elem and link_elem.text in media]
	except BaseException as e:
		print("link_elems error \n", str(e))
		raise NoSuchElementException
	if is_random:
		links = random.sample(links, len(links))
	# pdb.set_trace()
	return links[:amount]


def update_user_data(browser, username, user_data):
	print('Updating data for {}'.format(username))
	# pdb.set_trace()	
	try: 
		browser.get('https://www.instagram.com/' + username)
		sleep(1)
		main_elem = browser.find_element_by_tag_name('main')
		link_elems = main_elem.find_elements_by_tag_name('a')
		if link_elems:
			followers = format_number(re.match(r'.*\s',link_elems[0].text).group())
			following = format_number(re.match(r'.*\s',link_elems[1].text).group())
			if followers and following and username not in user_data.keys():			
				print('Creating user data entry for {}: followers: {}, following: {}, ratio: {}, last_notification: {}, black_list: {}'.format(username, followers, following, following/float(followers), None, False))
				user_data[username] = {'followers': followers, 'following': following, 'ratio': following/float(followers), 'last_notification': None, 'black_list': False}
			elif followers and following:
				print('Updating user data entry for {}: followers: {}, following: {}, ratio: {}'.format(username, followers, following, following/float(followers)))
				user_data[username]['followers']  = followers
				user_data[username]['following'] = following
				user_data[username]['ratio'] = following/float(followers)
	except BaseException as e:
		print("Error: {}".format(str(e)))
		print('Updating user data entry for {}: black_list: {}'.format(username, True))
		if username not in user_data.keys():
			user_data[username]= {'black_list': True }
		else:
			user_data[username]['black_list'] = True
		raise NoSuchElementException

def update_user_data_timestamp(username, user_data):
	if username not in user_data.keys():
		user_data[username] = {'followers': None, 'following': None, 'ratio': None, 'last_notification': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), 'black_list': False}
		print('Creating user data entry for {}: followers: {}, following: {}, ratio: {}, last_notification {}, black_list: {}'.format(username, None, None, None, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), False))
	else:
		user_data[username]['last_notification'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		print('Updating user data last_notification timestamp for {} as: {}'.format(username, datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')))

def update_user_data_following_me_status(username, status, user_data):
	if username not in user_data.keys():
		# the code bellow assume that all the dict enries need to have the keys in them in order to be updates. Not true. all Nones can be removed. 
		user_data[username] = {'followers': None, 'following': None, 'ratio': None, 'last_notification': None, 'black_list': False, 'following_me': status}
		print('Creating user data entry for {}: followers: {}, following: {}, ratio: {}, last_notification {}, black_list: {}, following_me: {}'.format(username, None, None, None, None, False, status))
	else:
		user_data[username]['following_me'] = status
		print('Updating user data following_me for user {} as {}'.format(username, status))

def update_user_data_following_them_status(username, status, user_data):
	if username not in user_data.keys():
		# the code bellow assume that all the dict enries need to have the keys in them in order to be updates. Not true. all Nones can be removed. 
		user_data[username] = {'followers': None, 'following': None, 'ratio': None, 'last_notification': None, 'black_list': False, 'following_them': status}
		print('Creating user data entry for {}: followers: {}, following: {}, ratio: {}, last_notification {}, black_list: {}, following_them: {}'.format(username, None, None, None, None, False, status))
	else:
		user_data[username]['following_them'] = status
		print('Updating user data following_them for user {} as {}'.format(username, status))


def format_number(number_as_string):
	number_as_string = number_as_string.strip()
	number_as_string = number_as_string.replace(',' , '')
	if number_as_string[-1] == 'k':
		number_as_string = number_as_string.replace('k', '00').replace('.', '')
	if number_as_string[-1] == 'm':
		number_as_string = number_as_string.replace('m', '00000').replace('.', '')
	try: 
		return int(number_as_string)
	except ValueError as e:
		print("Error parsing number")




def scroll_bottom(browser, element, range_int):
	num_elements = 0 
	for i in range(int(range_int / 2)):        
		if num_elements != len(browser.find_elements_by_xpath("//div/div/span/button[text()='Following']")) and i != 0:            
			num_elements = len(browser.find_elements_by_xpath("//div/div/span/button[text()='Following']"))
			browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)            
			time.sleep(randint(1,3))
	return

def get_media_formats(media):
	# pdb.set_trace()
	result = None
	if media is None:
		# All known media types
		result = ['', 'Post', 'Video']
	elif media == 'Photo':
		# Include posts with multiple images in it
		result = ['', 'Post']
	else:
		# Make it an array to use it in the following part
		result = [media]
	return result 
