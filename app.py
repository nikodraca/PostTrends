from flask import Flask, Markup, request, render_template, redirect
import requests
import json 
import time
import math
import datetime
import creds
from collections import Counter
import difflib

app = Flask(__name__)

@app.route('/')
def home():
	return "home page"

@app.route('/u/<user_input>')
def get_data(user_input):
	# Username -> id
	user = requests.get("https://api.instagram.com/v1/users/search?q=%s&access_token=%s" % (user_input, creds.ACCESS_TOKEN))

	if not (user.json()['data']):
		print "ok"
		return "Error loading profile. Make sure profile is public and exists."
	else:
		user_id = closest_match(user.json()['data'], user_input)

	if not user_id:
		return "Error. No match"


	# Make request for user info

	user_request = requests.get("https://api.instagram.com/v1/users/%s/?access_token=%s" % (user_id, creds.ACCESS_TOKEN))
	
	if user_request.json()['meta']['code'] == 400:
		return "Error loading profile. Make sure profile is public and exists."

	# Get user info as dict, used to populate
	user_info = user_request.json()['data']

	# Get media data for last 20 posts
	if user_request.json()['data']['counts']['media'] == 0:
		return "Error. No media."

	media_request = requests.get("https://api.instagram.com/v1/users/%s/media/recent/?access_token=%s&count=20" % (user_id, creds.ACCESS_TOKEN))

	# return json.dumps(media_request.json()['data'])

	likes = []
	comments = []
	days = []
	hours = []
	filters = []
	locations = []
	tags = []
	tag_positions = []

	# Loop and get relevant data
	for i in range(0, 20):
		try:
			likes.append(media_request.json()['data'][i]['likes']['count'])
			comments.append(media_request.json()['data'][i]['comments']['count'])
			days.append(datetime.datetime.fromtimestamp(int(media_request.json()['data'][i]['created_time'])).strftime('%a'))
			hours.append(datetime.datetime.fromtimestamp(int(media_request.json()['data'][i]['created_time'])).strftime('%H'))
			filters.append(media_request.json()['data'][i]['filter'])
			locations.append([media_request.json()['data'][i]['location']['latitude'], media_request.json()['data'][i]['location']['longitude']])		
			
			for x in range(0, len(media_request.json()['data'][i]['users_in_photo'])):
				tags.append([media_request.json()['data'][i]['users_in_photo'][x]['user']['username'], media_request.json()['data'][i]['users_in_photo'][x]['user']['id']])
				tag_positions.append([media_request.json()['data'][i]['users_in_photo'][x]['position']['x'], media_request.json()['data'][i]['users_in_photo'][x]['position']['y']])
		
		except (KeyError, TypeError, IndexError) as e:
			pass

	all_data = {}
	all_data['basic'] = user_info
	all_data['likes'] = list(reversed(likes)) 
	all_data['comments'] = list(reversed(comments))
	all_data['days'] = dict(Counter(days))
	all_data['hours'] = dict(Counter(hours))
	all_data['filters'] = dict(Counter(filters))
	all_data['locations'] = locations
	all_data['tags'] = tags
	all_data['tag_positions'] = tag_positions

	return render_template('chart.html', all_data=all_data)

def closest_match(obj, match):

	res = None

	for i in range(0,len(obj)):
		if obj[i]['username'] == match:
			res = obj[i]['id']
			break

	return res

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
