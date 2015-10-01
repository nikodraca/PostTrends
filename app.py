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
df = None
hm = None
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

@app.route('/')
def home():
	return render_template('index.html')

@app.route("/")
def getdata(userinput):

	global followers
	global follows 
	global pd
	global lc
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


	# Average likes
	avg_likes = sum/20

	# Likes Count
	lc = []

	for x in range(0,n):
		try:
			likes = int((adata['data'][x]['likes']['count']))
			lc.append(likes)
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"

	# Post Dates
	pd = []

	for x in range(0,n):
		try:
			postdates = int((adata['data'][x]['created_time']))
			postdatesvar = str(time.strftime("%D", time.localtime(postdates)))
			pd.append(postdatesvar)
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"

	# Day frequency
	df = []

	for x in range(0,n):
		try:
			postdates = int((adata['data'][x]['created_time']))
			postdatesvar = str(time.ctime(postdates)).split(" ")[0]
			df.append(postdatesvar)
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"


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



	hmc = []

	# Get hour frequency labels
	for x in range(0,24):
		hmc.append(hm.count(str(x)))

	# Hashtags popularity

	htgs = []
	htgsfinal = []

	# Find non-empty hashtags

	for x in range(0,n):
		try:
			hashlen = len(adata['data'][x]['tags'])
			hashtags = adata['data'][x]['tags']

			for item in hashtags:
				htgs.append(item)
		except IndexError:
			captionserrormsg = "Not enough posts to give significant analysis, sorry!"

	# Remove duplicates

	hdup1 = htgs
	hdup2 = htgs

	for hdup1 in hdup2:
	       if hdup1 not in htgsfinal:
	          htgsfinal.append(hdup1)

	htgscount = []

	# Retrieve counts


	# for item in htgsfinal:
	# 	t = requests.get('https://api.instagram.com/v1/tags/'+item+'/?access_token=8593252.c09ec1a.83deea9350bf4bb39f82c5937c86e56b')
	# 	t.text
	# 	tdata = json.loads(t.text)
	# 	logt = math.log(int(tdata['data']['media_count']),10)
	# 	htgscount.append(logt)
	# 	print logt

	for item in htgsfinal:
		try:
			t = requests.get('https://api.instagram.com/v1/tags/'+item+'/?access_token=8593252.c09ec1a.83deea9350bf4bb39f82c5937c86e56b')
			t.text
			tdata = json.loads(t.text)
			logt = math.log(int(tdata['data']['media_count']),10)
			htgscount.append(logt)
			hashtagerrormsg = ""

		except KeyError:
			htgscount.append(0)


	# Find variables
	# name = (data['data']['full_name'])
	posts = (data['data']['counts']['media'])
	followers = (data['data']['counts']['followed_by'])
	follows = (data['data']['counts']['follows'])
	try:
		ratio = round(float(followers)/float(follows),2)
		zeroerrormsg = ""


	except ZeroDivisionError:
		ratio = "0"
		zeroerrormsg = ", follows nobody"

	# Max height of barchart
	try:
		max_height = max(lc)
		max_heightJS = int(max_height) + (int(max_height)*0.30)

		max_height2 = max(htgscount)
		max_height2JS = int(max_height2) + (int(max_height2)*0.20)
	except ValueError:
		max_height2JS = 0
		hashtagerrormsg = "no hashtags used"



@app.route("/chart")
def chart():
    userinput = request.args.get('username', '')
    getdata(userinput)
    labels = ["Followers","Follows"]
    values = [followers,follows]
    colors = ["#60B9CE","#FF8373"]
    labels2 = pd
    values2 = lc
    labels3 = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    values3 = [moncount,tuecount,wedcount,thucount,fricount,satcount,suncount]
    labels4 = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00',]
    values4 = hmc
    labels5 = htgsfinal
    values5 = htgscount
    return render_template('chart.html', set=zip(values, labels, colors), userinput=userinput, avg_likes=avg_likes, posts=posts, followers=followers, follows=follows, values2=values2, labels2=labels2, max_heightJS=max_heightJS, max_height2JS=max_height2JS, ratio=ratio, values3=values3, labels3=labels3,
    						values4=values4, labels4=labels4, values5=values5, labels5=labels5, hashtagerrormsg=hashtagerrormsg, zeroerrormsg=zeroerrormsg, usererrormessage=usererrormessage)

# @app.route('/name')
# def whatever():
# 	return render_template('chart.html', name=name)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
