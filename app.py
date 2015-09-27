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
u = requests.get("https://api.instagram.com/v1/users/search?q="+userinput+"/&access_token=ACCESS_TOKEN")
u.text


udata = json.loads(u.text)

userid = (udata['data'][0]['id'])

# Get account info
a = requests.get('https://api.instagram.com/v1/users/'+userid+'/media/recent/?access_token=ACCESS_TOKEN&count=250')
r = requests.get('https://api.instagram.com/v1/users/'+userid+'/?access_token=ACCESS_TOKEN')
r.text
a.text

adata = json.loads(a.text)
data = json.loads(r.text)


n = 11
sum = 0

#  Like count
for x in range(0,n): 
	captions = int((adata['data'][x]['likes']['count']))
	sum = sum + captions

# Average likes
avg_likes = sum/10

# 
for x in range(0,n):
	likes = int((adata['data'][x]['likes']['count']))
	likesvar = likes
	print likesvar

for x in range(0,n):
	postdates = int((adata['data'][x]['created_time']))
	postdatesvar = time.strftime("%D", time.localtime(postdates))
	print postdatesvar



# Find variables
name = (data['data']['full_name'])
posts = (data['data']['counts']['media'])
followers = (data['data']['counts']['followed_by'])
follows = (data['data']['counts']['follows'])

# # Stats

# print "name:",name
# print "posts:",posts
# print "followers:",followers
# print "follows:",follows
# print "average likes (last 10 posts):", avg_likes

@app.route("/")
def chart():
    labels = ["Followers","Follows"]
    values = [followers,follows]
    colors = ["#46BFBD","#F7464A"]
    labels2 = [postdatesvar]
    values2 = [likesvar]
    return render_template('chart.html', set=zip(values, labels, colors), name=name, avg_likes=avg_likes, posts=posts, followers=followers, follows=follows,values2=values2, labels2=labels2)


# @app.route('/name')
# def whatever():
# 	return render_template('chart.html', name=name)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)









