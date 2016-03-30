from flask import Flask
from flask import Markup
from flask import request
from flask import Flask
from flask import render_template
from flask import redirect
import requests
import json 
import time
import math

app = Flask(__name__)


class allVars():
	followers = None
	follows = None
	pd = None
	lc = None
	cc = None
	df = None
	hm = None
	fc = None
	nodupfc = None
	fcc = None
	avg_likes = None
	posts = None
	max_heightJS = None
	max_height2JS = None
	ratio = None
	moncount = None
	tuecount = None
	wedcount = None
	thucount = None
	fricount = None
	satcount = None
	suncount = None
	hmc = None
	htgs = None
	htgsfinal = None
	hdup1 = None
	hdup2 = None
	htgscount = None
	logt = None
	hashtagerrormsg = ""
	zeroerrormsg = ""
	usererrormessage = ""
	nodupbff = None
	max_heightfilterJS = None
	bffcount = None
	averagetagcount = None
	geolat = None
	geolong = None
	geolatlen = None
	geoname = None


@app.route('/')
def home():
	return render_template('index.html')

@app.route("/")
def getdata(userinput):

	# Convert username to ID
	user_info = requests.get("https://api.instagram.com/v1/users/search?q="+userinput+"/&access_token=ACCESS_TOKEN")
	user_info.text
	udata = json.loads(user_info.text)

	try:
		user_id = (udata['data'][0]['id'])
		usererrormessage = ''

	except IndexError:
		user_id = '25025320'
		usererrormessage = " User not found, here's Instagram instead!"



	# Get media info
	media = requests.get('https://api.instagram.com/v1/users/'+user_id+'/media/recent/?access_token=ACCESS_TOKEN&count=250')
	media_data = json.loads(media.text)

	# Get profile info
	profile = requests.get('https://api.instagram.com/v1/users/'+user_id+'/?access_token=ACCESS_TOKEN')
	profile_data = json.loads(profile.text)


	# Set limit
	POST_MAX = 20
	likes_sum = 0


	# Find total likes count
	for x in range(0,POST_MAX):
		try:
			captions = int((media_data['data'][x]['likes']['count']))
			likes_sum = likes_sum + captions
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, try another profile?"
		except KeyError:
			user_id = '25025320'
			usererrormessage = " User private, here's Instagram instead!"



	# Average likes
	allVars.avg_likes = likes_sum/POST_MAX


	# Find likes/comments/filters/tagged friends count per post
	allVars.lc = []
	allVars.cc = []
	allVars.fc = []
	allVars.bff = []

	for x in range(0,POST_MAX):
		try:
			likes = int((media_data['data'][x]['likes']['count']))
			allVars.lc.append(likes)

			commentcount  = int((media_data['data'][x]['comments']['count']))
			allVars.cc.append(commentcount)

			filters  = (media_data['data'][x]['filter'])
			allVars.fc.append(filters)

			bestfriends = (media_data['data'][x]['users_in_photo'])
			try:
				for x in range(0,100):
					bestfriendsindex = bestfriends[x]['user']['username']
					allVars.bff.append(bestfriendsindex)
			except IndexError:
				bfferrormsg = "whoops"

		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, try another account?"

		except KeyError:
			user_id = '25025320'
			usererrormessage = " (User private)"




	# Geolocation info
	allVars.geolat = []
	allVars.geolong = []
	allVars.geoname = []

	for i in range(0,21):
		try:
			lats = media_data['data'][i]['location']['latitude']
			longs = media_data['data'][i]['location']['longitude']
			names = media_data['data'][i]['location']['name']
			allVars.geolat.append(lats)
			allVars.geolong.append(longs)
			allVars.geoname.append(names.encode('ascii', 'ignore'))

		except TypeError:
			errormsssg = ""
		except KeyError:
			errormsssg = ""
		except IndexError:
			errormsssg = ""

	allVars.geolatlen = len(allVars.geolat)


	# Remove duplicates
	allVars.nodupfc = list(set(allVars.fc))
	allVars.nodupbff = list(set(allVars.bff))


	# Filter/tag counts
	allVars.fcc = []
	allVars.bffval = []

	for item in allVars.nodupfc:
		allVars.fcc.append(allVars.fc.count(item))

	for item in allVars.nodupbff:
		allVars.bffval.append(int(allVars.bff.count(item)))

	allVars.bffcount = len(allVars.nodupbff)
	allVars.averagetagcount = round(float(allVars.bffcount/20.0),2)



	# Get all post dates
	allVars.pd = []

	for x in range(0,POST_MAX):
		try:
			postdates = int((media_data['data'][x]['created_time']))
			postdatesvar = str(time.strftime("%D", time.localtime(postdates)))
			allVars.pd.append(postdatesvar)
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"
		except KeyError:
			user_id = '25025320'
			usererrormessage = " (User private)"


	# Day frequency
	allVars.df = []

	for x in range(0,POST_MAX):
		try:
			postdates = int((media_data['data'][x]['created_time']))
			postdatesvar = str(time.ctime(postdates)).split(" ")[0]
			allVars.df.append(postdatesvar)
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"
		except KeyError:
			user_id = '25025320'
			usererrormessage = " (User private)"

	allVars.moncount = int(allVars.df.count("Mon"))
	allVars.tuecount = int(allVars.df.count("Tue"))
	allVars.wedcount = int(allVars.df.count("Wed"))
	allVars.thucount = int(allVars.df.count("Thu"))
	allVars.fricount = int(allVars.df.count("Fri"))
	allVars.satcount = int(allVars.df.count("Sat"))
	allVars.suncount = int(allVars.df.count("Sun"))



	# Hour frequency
	# First convert UNIX to readable date
	allVars.hm = []

	for x in range(0,POST_MAX):
		try:
			postdates = int((media_data['data'][x]['created_time']))
			postdatesvar = str(time.strftime("%H", time.localtime(postdates)))
			allVars.hm.append(postdatesvar)
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"
		except KeyError:
			user_id = '25025320'
			usererrormessage = " (User private)"



	# Get hour frequency labels
	allVars.hmc = []

	for x in range(0,24):
		allVars.hmc.append(allVars.hm.count(str(x)))



	# Handle errors
	try:
		posts = (profile_data['data']['counts']['media'])
	except KeyError:
		posts = 0
		usererrormessage = " (User private)"
	try:
		allVars.followers = (profile_data['data']['counts']['followed_by'])
	except KeyError:
		allVars.followers = 0
		usererrormessage = " (User private)"
	try:
		allVars.follows = (profile_data['data']['counts']['follows'])
	except KeyError:
		allVars.follows = 0
		usererrormessage = " (User private)"
	try:
		allVars.ratio = round(float(allVars.followers)/float(allVars.follows),2)
		zeroerrormsg = ""
	except ZeroDivisionError:
		allVars.ratio = "0"
		zeroerrormsg = ". No follows"


	# Max height of barchart
	try:
		allVars.max_height = max(allVars.lc)
		allVars.max_heightfilter = max(allVars.fcc)
		allVars.max_heightJS = int(allVars.max_height) + (int(allVars.max_height)*0.30)
		allVars.max_heightfilterJS = int(allVars.max_heightfilter) + (int(allVars.max_heightfilter)*0.30)
	except ValueError:
		print ""



@app.route("/chart")
def chart():
    userinput = request.args.get('username', '')
    getdata(userinput)
    labels = ["Followers","Follows"]
    values = [allVars.followers,allVars.follows]
    colors = ["rgba(151,187,205,1)","rgba(238,98,98,1)"]
    labels2 = allVars.pd
    values2 = allVars.lc
    values2_1 = allVars.cc
    labels3 = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    values3 = [allVars.moncount, allVars.tuecount, allVars.wedcount, allVars.thucount, allVars.fricount, allVars.satcount, allVars.suncount]
    labels4 = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00',]
    values4 = allVars.hmc
    labels5 = allVars.nodupfc
    values5 = allVars.fcc
    return render_template('chart.html', set=zip(values, labels, colors), userinput=userinput, avg_likes=allVars.avg_likes, posts=allVars.posts, followers=allVars.followers, follows=allVars.follows, values2=values2, values2_1=values2_1, labels2=labels2,
    						 max_heightJS=allVars.max_heightJS, max_height2JS=allVars.max_height2JS, max_heightfilterJS=allVars.max_heightfilterJS,ratio=allVars.ratio, values3=values3, labels3=labels3, values4=values4, labels4=labels4, zeroerrormsg=allVars.zeroerrormsg,
    						 usererrormessage=allVars.usererrormessage, values5=values5, labels5=labels5, nodupbff=allVars.nodupbff, bffcount=allVars.bffcount, averagetagcount=allVars.averagetagcount, geolong=allVars.geolong, geolat=allVars.geolat,geolatlen=allVars.geolatlen, geoname=allVars.geoname)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
