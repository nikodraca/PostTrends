from flask import Flask
from flask import Markup
from flask import request
from flask import Flask
from flask import render_template
from flask import redirect
import requests
import json
import time

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
ratio = None
moncount = None
tuecount = None
wedcount = None
thucount = None
fricount = None
satcount = None
suncount = None
hmc = None

# @app.route('/')
# def my_form():
#     return render_template("index.html")

# @app.route('/', methods=['GET'])
# def my_form_post():
#     text = request.form['username']
#     getdata(text)

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
	global ratio
	global moncount
	global tuecount
	global wedcount
	global thucount
	global fricount
	global satcount
	global suncount

	# Enter your user name
	# userinput = raw_input("Enter a user name: ")

	# Convert username to ID
	u = requests.get("https://api.instagram.com/v1/users/search?q="+userinput+"/&access_token=AT")
	u.text


	udata = json.loads(u.text)

	userid = (udata['data'][0]['id'])

	# Get account info
	a = requests.get('https://api.instagram.com/v1/users/'+userid+'/media/recent/?access_token=AT&count=250')
	r = requests.get('https://api.instagram.com/v1/users/'+userid+'/?access_token=AT')
	r.text
	a.text

	adata = json.loads(a.text)
	data = json.loads(r.text)


	n = 20
	sum = 0

	for x in range(0,n): 
		captions = int((adata['data'][x]['likes']['count']))
		sum = sum + captions

	# Average likes
	avg_likes = sum/20

	# Likes Count
	lc = []

	for x in range(0,n):
		likes = int((adata['data'][x]['likes']['count']))
		lc.append(likes)

	# Post Dates
	pd = []

	for x in range(0,n):
		postdates = int((adata['data'][x]['created_time']))
		postdatesvar = str(time.strftime("%D", time.localtime(postdates)))
		pd.append(postdatesvar)

	# Day frequency
	df = []

	for x in range(0,n):
		postdates = int((adata['data'][x]['created_time']))
		postdatesvar = str(time.ctime(postdates)).split(" ")[0]
		df.append(postdatesvar)

	moncount = int(df.count("Mon"))
	tuecount = int(df.count("Tue"))
	wedcount = int(df.count("Wed"))
	thucount = int(df.count("Thu"))
	fricount = int(df.count("Fri"))
	satcount = int(df.count("Sat"))
	suncount = int(df.count("Sun"))


	hm = []

	for x in range(0,n):
		postdates = int((adata['data'][x]['created_time']))
		postdatesvar = str(time.strftime("%H", time.localtime(postdates)))
		hm.append(postdatesvar)

	hmc = []

	for x in range(0,24):
		hmc.append(hm.count(str(x)))


	# Find variables
	# name = (data['data']['full_name'])
	posts = (data['data']['counts']['media'])
	followers = (data['data']['counts']['followed_by'])
	follows = (data['data']['counts']['follows'])
	ratio = round(float(followers)/float(follows),2)

	# Max height of barchart
	max_height = max(lc)
	max_heightJS = int(max_height) + (int(max_height)*0.30)



@app.route("/chart")
def chart():
    userinput = request.args.get('username', '')
    getdata(userinput)
    labels = ["Followers","Follows"]
    values = [followers,follows]
    colors = ["#46BFBD","#F7464A"]
    labels2 = pd
    values2 = lc
    labels3 = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    values3 = [moncount,tuecount,wedcount,thucount,fricount,satcount,suncount]
    labels4 = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00',]
    values4 = hmc
    return render_template('chart.html', set=zip(values, labels, colors), userinput=userinput, avg_likes=avg_likes, posts=posts, followers=followers, follows=follows, values2=values2, labels2=labels2, max_heightJS=max_heightJS, ratio=ratio, values3=values3, labels3=labels3, values4=values4, labels4=labels4)

# @app.route('/name')
# def whatever():
# 	return render_template('chart.html', name=name)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)









