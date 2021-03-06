# clarifai
"""Module which handles the clarifai api and checks
the image for invalid content"""
from clarifai.rest import ClarifaiApp, Image as ClImage
from os import environ
import operator
import pdb
import json 


clarifai_api_key = 'c697787ce28e4c94a2e8214c01dd9385'

def check_image(browser):
	"""Uses the link to the image to check for invalid content in the image"""
	# pdb.set_trace()	
	clarifai_api = ClarifaiApp(api_key=clarifai_api_key)

	img_link = get_imagelink(browser)
	# Uses Clarifai's v2 API
	model = clarifai_api.models.get('general-v1.3')
	image = ClImage(url=img_link)
	result = model.predict([image])
	result = result['outputs'][0]

	# Get all the clarify tags and names in the format (name, confidence)
	clarifai_tags = []
	for i in range(len(result['data']['concepts'])):
		concept = result['data']['concepts'][i]
		concept_t = (concept['name'], concept['value'])
		clarifai_tags.append(concept_t)

	# Get the top number of tages sorted by the confidence interval
	top = 10
	top_tag_tup = sorted(clarifai_tags, key=operator.itemgetter(1))[-top:]
	top_just_names = [t[0] for t in top_tag_tup]
	
	return True, top_just_names


def get_imagelink(browser):
	"""Gets the imagelink from the given webpage open in the browser"""
	return browser.find_element_by_xpath('//img[@class = "_2di5p"]') \
		.get_attribute('src')

