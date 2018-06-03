# Manager class 
from browser import Browser
#from pyvirtualdisplay import Display
from notifications import Notifications
from follower import Follower 
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
			random_tags = random.sample(tags, 5)
			self.commenter.comment_by_tag(random_tags, 5, True)
			sleep_time = random.randint(1, 20)
			print('Sleeping for {} starting at {}'.format(sleep_time, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
			time.sleep(60 * sleep_time) 

	def follow_strategy(self):
		self.follower = Follower(self.browser, self.username)
		# self.follower.report()
		# self.follower.update_followers()
		# self.follower.update_following()
		# self.follower.engage_with_followers_followers()
		self.follower.engage_with_feed()

	def follow_strategy_mix(self):
		self.follower = Follower(self.browser, self.username)
		self.notification_manager = Notifications(self.browser, self.username)
		self.follower.report()
		while True: 
			self.notification_manager.notifications()
			self.notification_manager.save_data()
			self.follower.engage_with_followers_followers()		
			sleep_time = random.randint(1, 10)
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
	'superhubs','visualcreators','artofvisuals','aov','createcommune',
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

	tags2 = ['createexploretakeover', 'mkexplore', 'killeverygram', 'urbanandstreet', 'hsdailyfeature', 'hbouthere', 'aov', 'meistershots', 'uncalculated', 'yngkillers', 'streetmobs', 'citykillerz', 'visualsgang', 'visualarchitects', 'streetshared', 'instamagazine_', 'estheticlabel', 'streetmagazine', 'visualambassadors', 'highsnobiety', 'gearednomad', 'createyourhype', 'shotzdelight', 'streetactivity', 'instagoodmyphoto', 'primeshots', '1stinstinct', 'symmetricalmonsters', 'postthepeople', 'imaginatones', 'toronto', 'torontolife', 'the6ix', 'canada', 'yyz', 'the6', 'thesix', '416', 'tdot', '6ix', 'streetsoftoronto', 'lovetoronto', 'torontophoto', 'ontario', 'mississauga', 'igerstoronto', 'blogto', 'toronto_insta', 'torontoigers', 'thankyoutoronto', 'wethenorth', 'downtowntoronto', 'torontofashion', 'torontofood', '6ixwalks', 'scarborough', 'brampton', 'imagesoftoronto', 'gta', 'torontophotography', 'urbanandstreet', 'aov', 'yngkillers', 'killeverygram', 'citykillerz', 'meistershots', 'shotzdelight', 'ig_color', 'streetmobs', 'mkexplore', 'createexploretakeover', 'streetshared', 'streetmagazine', 'gearednomad', 'visualambassadors', 'folkgood', 'hsdailyfeature', 'vzcomood', 'uncalculated', 'visualsgang', 'weekly_feature', 'mg5k', 'imaginatones', 'symmetricalmonsters', 'visualarchitects', 'hbouthere', 'instagoodmyphoto', 'rsa_streetview', 'portraitpage', 'usaprimeshot']

	# Run the notification module 
	# session.notification_manager()
	session.mix_comments_notifications(tags2) 
	# session.commenter_lables(tags_lecon, 2)
	
	# session.follow_strategy_mix()
	# session.follow_strategy()

