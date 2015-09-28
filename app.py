from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
import requests
import json
import time

app = Flask(__name__)

# Enter your user name
# userinput = raw_input("Enter a user name: ")
userinput = "user"

# Convert username to ID
u = requests.get("https://api.instagram.com/v1/users/search?q="+userinput+"/&access_token=")
u.text


udata = json.loads(u.text)

userid = (udata['data'][0]['id'])

# Get account info
a = requests.get('https://api.instagram.com/v1/users/'+userid+'/media/recent/?access_token=&count=250')
r = requests.get('https://api.instagram.com/v1/users/'+userid+'/?access_token=')
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

count1 = int(hm.count("1"))
count2 = int(hm.count("2"))
count3 = int(hm.count("3"))
count4 = int(hm.count("4"))
count5 = int(hm.count("5"))
count6 = int(hm.count("6"))
count7 = int(hm.count("7"))
count8 = int(hm.count("8"))
count9 = int(hm.count("9"))
count10 = int(hm.count("10"))
count11 = int(hm.count("11"))
count12 = int(hm.count("12"))
count13 = int(hm.count("13"))
count14 = int(hm.count("14"))
count15 = int(hm.count("15"))
count16 = int(hm.count("16"))
count17 = int(hm.count("17"))
count18 = int(hm.count("18"))
count19 = int(hm.count("19"))
count20 = int(hm.count("20"))
count21 = int(hm.count("21"))
count22 = int(hm.count("22"))
count23 = int(hm.count("23"))
count24 = int(hm.count("24"))



# Find variables
name = (data['data']['full_name'])
posts = (data['data']['counts']['media'])
followers = (data['data']['counts']['followed_by'])
follows = (data['data']['counts']['follows'])
ratio = round(float(followers)/float(follows),2)

# Max height of barchart
max_height = max(lc)
max_heightJS = int(max_height) + (int(max_height)*0.30)


@app.route("/")
def chart():
    labels = ["Followers","Follows"]
    values = [followers,follows]
    colors = ["#46BFBD","#F7464A"]
    labels2 = pd
    values2 = lc
    labels3 = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    values3 = [moncount,tuecount,wedcount,thucount,fricount,satcount,suncount]
    labels4 = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00',]
    values4 = [count24, count1, count2, count3, count4, count5, count6, count7, count8, count9, count10, count11, count12, count13, count14, count15, count16, count17, count18, count19, count20, count21, count22, count23,]
    return render_template('chart.html', set=zip(values, labels, colors), name=name, avg_likes=avg_likes, posts=posts, followers=followers, follows=follows, values2=values2, labels2=labels2, max_heightJS=max_heightJS, ratio=ratio, values3=values3, labels3=labels3, values4=values4, labels4=labels4)


# @app.route('/name')
# def whatever():
# 	return render_template('chart.html', name=name)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)









