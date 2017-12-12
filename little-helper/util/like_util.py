# like_util
import random
from math import ceil
from .time_util import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


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

def get_links_for_username(browser, username, amount, is_random=False, media=None):
	"""Fetches the number of links specified
		by amount and returns a list of links
		Raises: NoSuchElementException
	"""
	if media is None:
		# All known media types
		media = ['', 'Post', 'Video']
	elif media == 'Photo':
		# Include posts with multiple images in it
		media = ['', 'Post']
	else:
		# Make it an array to use it in the following part
		media = [media]



	print('Attempting to get image list for {}/'.format(username))
	browser.get('https://www.instagram.com/' + username)
	sleep(2)
	body_elem = browser.find_element_by_tag_name('body')
	try:
		is_private = body_elem.find_element_by_xpath('//h2[@class="_kcrwx"]')
		if is_private:
			print('This user is private...')
			return False
	except:
		print('Beginning interaction')	
	sleep(2)

	# Clicking load more
	abort = True
	try:
		load_button = body_elem.find_element_by_xpath( '//a[contains(@class, "_1cr2e _epyes")]')
		abort = False
		body_elem.send_keys(Keys.END)
		sleep(2)
		load_button.click()
	except:
		print('Load button not found, working with current images!')
	body_elem.send_keys(Keys.HOME)
	sleep(2)


	# Get Links
	try:
		main_elem = browser.find_element_by_tag_name('main')
		link_elems = main_elem.find_elements_by_tag_name('a')
		total_links = len(link_elems)
		links = []
		filtered_links = 0
		if link_elems:
			links = [link_elem.get_attribute('href') for link_elem in link_elems
					if link_elem and link_elem.text in media]
			filtered_links = len(links)
	except BaseException as e:
		print("link_elems error \n", str(e))
		raise NoSuchElementException

	if is_random:
		# Expanding the poulation for better random distribution
		amount = amount * 5


	while (filtered_links < amount) and not abort:
		amount_left = amount - filtered_links
		# Average items of the right media per page loaded
		new_per_page = ceil(12 * filtered_links / total_links)
		if new_per_page == 0:
			# Avoid division by zero
			# Number of page load needed
			new_per_page = 1. / 12. 
		# Don't go bananas trying to get all of instagram!
		new_needed = min(int(ceil(amount_left / new_per_page)), 12)
		for i in range(new_needed):  # add images x * 12
			# Keep the latest window active while loading more posts
			before_load = total_links
			body_elem.send_keys(Keys.END)
			sleep(1)
			body_elem.send_keys(Keys.HOME)
			sleep(1)
			link_elems = main_elem.find_elements_by_tag_name('a')
			total_links = len(link_elems)
			abort = (before_load == total_links)
			if abort:
				break

		links = [link_elem.get_attribute('href') for link_elem in link_elems
				if link_elem.text in media]
		filtered_links = len(links)

	if is_random:
		# Shuffle the population index
		links = random.sample(links, filtered_links)

	return links[:amount]

