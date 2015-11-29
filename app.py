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
followers = None
follows = None
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
hashtagerrormsg = None
zeroerrormsg = None
usererrormessage = None
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

@app.route('/purchase')
def purchase():
	return render_template('purchase.html')


@app.route("/")
def getdata(userinput):

	global followers
	global follows 
	global pd
	global lc
	global cc
	global df
	global hm
	global hmc
	global avg_likes
	global posts
	global followers
	global follows
	global max_heightJS
	global max_height2JS
	global ratio
	global moncount
	global tuecount
	global wedcount
	global thucount
	global fricount
	global satcount
	global suncount
	global htgs
	global htgsfinal
	global hdup1
	global hdup2
	global htgscount
	global logt
	global hashtagerrormsg
	global zeroerrormsg
	global usererrormessage
	global fc
	global nodupfc
	global fcc
	global nodupbff
	global max_heightfilterJS
	global bffcount
	global averagetagcount
	global geolat 
	global geolong
	global geolatlen
	global geoname


	# Enter your user name
	# userinput = raw_input("Enter a user name: ")

	# Convert username to ID
	u = requests.get("https://api.instagram.com/v1/users/search?q="+userinput+"/&access_token=")
	u.text


	udata = json.loads(u.text)

	try:
		userid = (udata['data'][0]['id'])
		usererrormessage = ''



	except IndexError:
		userid = '25025320'
		usererrormessage = " (User not found, here's Instagram instead!)"

	# Get account info
	a = requests.get('https://api.instagram.com/v1/users/'+userid+'/media/recent/?access_token=&count=250')
	r = requests.get('https://api.instagram.com/v1/users/'+userid+'/?access_token=')
	r.text
	a.text

	adata = json.loads(a.text)
	data = json.loads(r.text)


	n = 20
	sum = 0

	# Finding likes counts

	for x in range(0,n):
		try:
			captions = int((adata['data'][x]['likes']['count']))
			sum = sum + captions
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"
		except KeyError:
			userid = '25025320'
			usererrormessage = " (User private, here's Instagram instead!)"



	# Average likes
	avg_likes = sum/20

	# Likes Count
	lc = []
	cc = []
	fc = []
	bff = []
	geolat = []
	geolong = []
	geoname = []

	for x in range(0,n):
		try:
			likes = int((adata['data'][x]['likes']['count']))
			lc.append(likes)
			commentcount  = int((adata['data'][x]['comments']['count']))
			cc.append(commentcount)
			filters  = (adata['data'][x]['filter'])
			fc.append(filters)
			bestfriends = (adata['data'][x]['users_in_photo'])
			try:
				for x in range(0,100):
					bestfriendsindex = bestfriends[x]['user']['username']
					bff.append(bestfriendsindex)


			except IndexError:
				bfferrormsg = "whoops"

		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"
		except KeyError:
			userid = '25025320'
			usererrormessage = " (User private)"

		# Geolocation

	for i in range(0,21):
		try:
			lats = adata['data'][i]['location']['latitude']
			longs = adata['data'][i]['location']['longitude']
			names = adata['data'][i]['location']['name']
			geolat.append(lats)
			geolong.append(longs)
			geoname.append(names.encode('ascii', 'ignore'))

		except TypeError:
			errormsssg = ""
		except KeyError:
			errormsssg = ""
		except IndexError:
			errormsssg = ""

	geolatlen = len(geolat)


	nodupfc = list(set(fc))
	nodupbff = list(set(bff))

	fcc = []
	bffval = []

	for item in nodupfc:
		fcc.append(fc.count(item))

	for item in nodupbff:
		bffval.append(int(bff.count(item)))

	bffcount = len(nodupbff)
	averagetagcount = round(float(bffcount/20.0),2)

	# Post Dates
	pd = []

	for x in range(0,n):
		try:
			postdates = int((adata['data'][x]['created_time']))
			postdatesvar = str(time.strftime("%D", time.localtime(postdates)))
			pd.append(postdatesvar)
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"
		except KeyError:
			userid = '25025320'
			usererrormessage = " (User private)"


	# Day frequency
	df = []

	for x in range(0,n):
		try:
			postdates = int((adata['data'][x]['created_time']))
			postdatesvar = str(time.ctime(postdates)).split(" ")[0]
			df.append(postdatesvar)
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"
		except KeyError:
			userid = '25025320'
			usererrormessage = " (User private)"



	moncount = int(df.count("Mon"))
	tuecount = int(df.count("Tue"))
	wedcount = int(df.count("Wed"))
	thucount = int(df.count("Thu"))
	fricount = int(df.count("Fri"))
	satcount = int(df.count("Sat"))
	suncount = int(df.count("Sun"))


	# Hour frequency

	hm = []

	# Convert UNIX to readable date
	for x in range(0,n):
		try:
			postdates = int((adata['data'][x]['created_time']))
			postdatesvar = str(time.strftime("%H", time.localtime(postdates)))
			hm.append(postdatesvar)
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"
		except KeyError:
			userid = '25025320'
			usererrormessage = " (User private)"




	hmc = []

	# Get hour frequency labels
	for x in range(0,24):
		hmc.append(hm.count(str(x)))


	# Find variables
	try:
		posts = (data['data']['counts']['media'])
	except KeyError:
		posts = 0
		usererrormessage = " (User private)"
	try:
		followers = (data['data']['counts']['followed_by'])
	except KeyError:
		followers = 0
		usererrormessage = " (User private)"

	try:
		follows = (data['data']['counts']['follows'])
	except KeyError:
		follows = 0
		usererrormessage = " (User private)"

	try:
		ratio = round(float(followers)/float(follows),2)
		zeroerrormsg = ""

	except ZeroDivisionError:
		ratio = "0"
		zeroerrormsg = ", follows nobody"

	# Max height of barchart
	try:
		max_height = max(lc)
		max_heightfilter = max(fcc)
		max_heightJS = int(max_height) + (int(max_height)*0.30)
		max_heightfilterJS = int(max_heightfilter) + (int(max_heightfilter)*0.30)
	except ValueError:
		print ""


@app.route("/chart")
def chart():
    userinput = request.args.get('username', '')
    getdata(userinput)
    labels = ["Followers","Follows"]
    values = [followers,follows]
    colors = ["rgba(151,187,205,1)","rgba(238,98,98,1)"]
    labels2 = pd
    values2 = lc
    values2_1 = cc
    labels3 = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    values3 = [moncount,tuecount,wedcount,thucount,fricount,satcount,suncount]
    labels4 = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00',]
    values4 = hmc
    labels5 = nodupfc
    values5 = fcc
    return render_template('chart.html', set=zip(values, labels, colors), userinput=userinput, avg_likes=avg_likes, posts=posts, followers=followers, follows=follows, values2=values2, values2_1=values2_1, labels2=labels2,
    						 max_heightJS=max_heightJS, max_height2JS=max_height2JS, max_heightfilterJS=max_heightfilterJS,ratio=ratio, values3=values3, labels3=labels3, values4=values4, labels4=labels4, zeroerrormsg=zeroerrormsg,
    						 usererrormessage=usererrormessage, values5=values5, labels5=labels5, nodupbff=nodupbff, bffcount=bffcount, averagetagcount=averagetagcount, geolong=geolong, geolat=geolat,geolatlen=geolatlen, geoname=geoname)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
