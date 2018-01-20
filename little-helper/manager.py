# Manager class 
from browser import Browser
from notifications import Notifications
from datetime import datetime
from commenter import Commenter
from util.login_util import login_user
import random
import time



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

	def commenter(self, tags): 
		self.commenter = Commenter(self.browser, username)
		self.commenter.comment_by_tag(tags, 1, True)

	def commenter_lables(self, tags, amount=1): 
		self.commenter = Commenter(self.browser, username)
		self.commenter.make_clarifai_lable_file(tags, amount, engage_user=False)

	def mix_comments_notifications(self, tags):
		self.notification_manager = Notifications(self.browser, self.username)
		self.commenter = Commenter(self.browser, username)
		while True: 
			self.notification_manager.notifications()
			self.notification_manager.save_data()
			random_tags = random.sample(tags, 3)
			self.commenter.comment_by_tag(random_tags, 1, True)
			sleep_time = random.randint(5, 60)
			print('Sleeping for {} starting at {}'.format(sleep_time, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
			time.sleep(60 * sleep_time) 

			


if __name__ == '__main__': 

	# These will be removed. 
	username = 'with.eden'
	password = '438queenwest'











	# Log in with the manager 
	session = Manager(username, password)

	# Run the Commeter
	tags = ['snobshots','makeportraits','thecreatorclass','creativevagrants','agameoftones',
	'moodygrams','fatalframes','theimaged','urbangathering','way2ill','illgrammers','vsco','streetdreamsmag',
	'visualsgang','dailyfeatures','exploretocreate','theoutbound','createexplore','ig_color','ig_masterpiece',
	'superhubs','visualcreators','thecreatorclass','artofvisuals','aov','thecreatorclass','createcommune',
	'bnw_sniper','jointheclass','exploreeverything','visualarchitects','hsdailyfeature','hbouthere',
	'createexploretakeover','monochrome','explorecanada','hypebeast','liveauthentic','blackandwhite','makeadventure',
	'rsa_streetview','bnw','streetsoftoronto','lovetoronto','mobilemag','blackandwhiteisworththefight','fashion',
	'magazine','session','modeling','model','foto','models ','photographers','californialove','editorialphotography',
	'fashionphotographer','fashiondiaries','nextdoormodelmagazine','hamburg','male','lifestyle','ig_minimalist',
	'ig_minimalshots ','vscomood','igmasters','shotaward','lifestyleblogger','minimalism','minimal_perfection',
	'vscoaward','rsa_minimal ','ignant','exklusive_shot','naturallight','artnude','nudemodel',
	'tatooedmodel','girlswithtattoos','feminist','portrait','portraitmood','peoplescreatives','portraitphotography ',
	'toronto','torontomodel','internationalmodel','photooftheday','bestoftheday','beauty','makeupaddict','portraitpros',
	'seamyphotos','antmisback','wlyg','torontophotographer','photographer','fit','fitnessmodel','studiosessions',
	'lingire','fashionista','fashionblogger','fashionblog','fashionstyle','fashionlover','fashioninsta','fashiondaily',
	'fashionaddict','fblogger','ootd','outfitoftheday','outfitinspiration','outfitpost','style','styleoftheday',
	'styleinspiration','styletips','stylefile','styledbyme','lookbook','streetstyle','shopaholic','streetstyleluxe',
	'instafashion','nakidmagazine','portraitpage','portraits_ig ','lookslikefilm ',
	'expofilm','photographyislife','postmoreportraits','picoftheday','featuremebest','vsco ','vscostyle','vscoportrait',
	'folkcreative','hinfluencercollective','socality','visualauthority','discoverportrait','fashionphotography ','ftwotw',
	'pursuitofportraits','bleachmyfilm','portraitcollective ','featurepalette','postthepeople','photographyislife',
	'sombrebeings','goodvibes','finditliveit','shoes','kicks','kicks0l0gy','instakicks','sneakers','sneaker','sneakerhead',
	'sneakerheads','solecollector','soleonfire','nicekicks','igsneakercommunity','sneakerfreak','sneakerporn','sneakerfiend',
	'sneakershouts','kicksonfire','fresh','walklikeus','nike','sneakerholics','sneakerfiend','shoegasm','kickstagram',
	'jordan','nikeair','adidas','queenwest']
	# session.commenter(tags)

	tags_lecon = ['foodie', 'foodpost', 'foodporn', 'foodgasm', 'foodphotography', 'foodphoto', 'goodfood', 
	'gastropost', 'gastronomy', 'gastronomical', 'culinaryarts', 'culinaryculture', 'deliciousfood', 'localfood', 
	'locallysourced', 'flatlay', 'flatlayforever', 'flatlaylover', 'flatlayfever', 'healthyeating', 
	'healthyliving', 'healthycooking', 'torontoeats', 'torontofood', 'torontorestaurants', 'torontophoto', 
	'torontobars', 'torontofashion', 'torontomodel', 'torontostreetstyle', 'tasteoftoronto', 'womensstyle', 
	'womenswear', 'womensfashion', 'womensstreetstyle', 'womensstreetfashion', 'womenwithstyle', 
	'womenwithstreetstyle', 'womenwithclass', 'snobshots', 'justgoshoot', 'way2ill', 'moodyports', 'moodygrams', 
	'moodyphotography', 'highsnobiety', 'highsnobietyfashion', 'highsnobietystyle', 'hypebae', 'hypebeastfashion', 
	'hypebeaststyle', 'igerstoronto', 'narcitytoronto', 'explorecanada', '6ixgrams', 'luxurytravel', 'luxuryfood', 
	'luxuryhotel', 'luxurytrip', 'wanderlust', 'hotellife', 'staycation', 'boutiquehotel', 'luxuryliving', 
	'abstractart', 'abstractpose', 'abstractmodel', 'abstractphotography', 'visualsofart', 'visualsoflife']

	# Run the notification module 
	# session.notification_manager()
	session.mix_comments_notifications(tags) 
	# session.commenter_lables(tags_lecon, 2)
