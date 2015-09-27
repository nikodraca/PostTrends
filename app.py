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

#################################################### Post 1

likes = int((adata['data'][0]['likes']['count']))
likesvar = likes

postdates = int((adata['data'][0]['created_time']))
postdatesvar = time.strftime("%D", time.localtime(postdates))

#################################################### Post 2


likes1 = int((adata['data'][1]['likes']['count']))
likesvar1 = likes1

postdates1 = int((adata['data'][1]['created_time']))
postdatesvar1 = time.strftime("%D", time.localtime(postdates1))


#################################################### Post 3

likes2 = int((adata['data'][2]['likes']['count']))
likesvar2 = likes2

postdates2 = int((adata['data'][2]['created_time']))
postdatesvar2 = time.strftime("%D", time.localtime(postdates2))

#################################################### Post 4

likes3 = int((adata['data'][3]['likes']['count']))
likesvar3 = likes3

postdates3 = int((adata['data'][3]['created_time']))
postdatesvar3 = time.strftime("%D", time.localtime(postdates3))

#################################################### Post 5

likes4 = int((adata['data'][4]['likes']['count']))
likesvar4 = likes4

postdates4 = int((adata['data'][4]['created_time']))
postdatesvar4 = time.strftime("%D", time.localtime(postdates4))

#################################################### Post 6


likes5 = int((adata['data'][5]['likes']['count']))
likesvar5 = likes5

postdates5 = int((adata['data'][5]['created_time']))
postdatesvar5 = time.strftime("%D", time.localtime(postdates5))

#################################################### Post 7


likes6 = int((adata['data'][6]['likes']['count']))
likesvar6 = likes6

postdates6 = int((adata['data'][6]['created_time']))
postdatesvar6 = time.strftime("%D", time.localtime(postdates6))

#################################################### Post 8


likes7 = int((adata['data'][7]['likes']['count']))
likesvar7 = likes7

postdates7 = int((adata['data'][7]['created_time']))
postdatesvar7 = time.strftime("%D", time.localtime(postdates7))

#################################################### Post 9


likes8 = int((adata['data'][8]['likes']['count']))
likesvar8 = likes8

postdates8 = int((adata['data'][8]['created_time']))
postdatesvar8 = time.strftime("%D", time.localtime(postdates8))

#################################################### Post 10

likes9 = int((adata['data'][9]['likes']['count']))
likesvar9 = likes9

postdates9 = int((adata['data'][9]['created_time']))
postdatesvar9 = time.strftime("%D", time.localtime(postdates9))




# Find variables
name = (data['data']['full_name'])
posts = (data['data']['counts']['media'])
followers = (data['data']['counts']['followed_by'])
follows = (data['data']['counts']['follows'])
ratio = round(float(followers)/float(follows),2)


max_height = max(likes,likes1, likes2)
max_heightJS = int(max_height) + (int(max_height)*0.30)

@app.route("/")
def chart():
    labels = ["Followers","Follows"]
    values = [followers,follows]
    colors = ["#46BFBD","#F7464A"]
    labels2 = [postdatesvar,postdatesvar1,postdatesvar2,postdatesvar3,postdatesvar4,postdatesvar5,postdatesvar6,postdatesvar7,postdatesvar8,postdatesvar9]
    values2 = [likesvar,likesvar1,likesvar2,likesvar3,likesvar4,likesvar5,likesvar6,likesvar7,likesvar8,likesvar9]
    return render_template('chart.html', set=zip(values, labels, colors), name=name, avg_likes=avg_likes, posts=posts, followers=followers, follows=follows,values2=values2, labels2=labels2, max_heightJS=max_heightJS, ratio=ratio)


# @app.route('/name')
# def whatever():
# 	return render_template('chart.html', name=name)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)









