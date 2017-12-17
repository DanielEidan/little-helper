# like_util
import random
from math import ceil
from .time_util import sleep
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
	"""Fetches the number of links specified type (type_flag='user'/'tag')
		by amount and returns a list of links
		Raises: NoSuchElementException
	"""
	media = get_media_formats(media)
	if type_flag == 'user':
		print('Attempting to get image list for {}'.format(username))
		browser.get('https://www.instagram.com/' + username)
	elif type_flag == 'tag':
		print('Attempting to get image for TAG {}/'.format(tag))		
		browser.get('https://www.instagram.com/explore/tags/' + (tag[1:] if tag[:1] == '#' else tag))		
	sleep(2)
	body_elem = browser.find_element_by_tag_name('body')
	sleep(2)

	links = []
	try:
		if type_flag == 'tag' and skip_top_posts:
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
	return links[:amount]


def update_user_data(browser, username, user_data):
	# pdb.set_trace()
	print('Updating data for {}'.format(username))	
	try: 
		browser.get('https://www.instagram.com/' + username)
		sleep(1)
		main_elem = browser.find_element_by_tag_name('main')
		link_elems = main_elem.find_elements_by_tag_name('a')
		if link_elems:
			followers = int(re.match(r'.*\s',link_elems[0].text).group().strip().replace(',' , ''))
			following = int(re.match(r'.*\s',link_elems[1].text).group().strip().replace(',' , ''))
		if username not in user_data.keys():			
			print('Creating user data entry: followers: {}, following: {}, ratio: {}'.format(followers, following, following/float(followers)))
			user_data[username] = {'followers': followers, 'following': following, 'ratio': following/float(followers)}
		else:
			print('Updating user data entry: followers: {}, following: {}, ratio: {}'.format(followers, following, following/float(followers)))
			user_data[username]['followers']  = followers
			user_data[username]['following'] = following
			user_data[username]['ratio'] = following/float(followers)
	except BaseException as e:
		print("Error \n", str(e))
		raise NoSuchElementException


def scroll_bottom(browser, element, range_int):
	num_elements = 0 
	for i in range(int(range_int / 2)):        
		if num_elements != len(browser.find_elements_by_xpath("//div/div/span/button[text()='Following']")) and i != 0:            
			num_elements = len(browser.find_elements_by_xpath("//div/div/span/button[text()='Following']"))                        
			browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)            
			time.sleep(randint(1,3))
	return

def get_media_formats(media):
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
