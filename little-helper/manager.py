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

	def commenter(self, tags): 
		self.commenter = Commenter(self.browser, username)		
		self.commenter.comment_by_tag(tags, 1)


if __name__ == '__main__': 

	# These will be removed. 
	username = ''
	password = ''

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

	# Run the notification module 
	session.notification_manager() 
