from flask import Flask, Markup, request, render_template, redirect
import requests
import json 
import time
import math
import datetime
import creds

app = Flask(__name__)

@app.route('/')
def get_data():
	# Username -> id
	user = requests.get("https://api.instagram.com/v1/users/search?q=%s&access_token=%s" % ("nikodraca", creds.ACCESS_TOKEN))

	if not (user.json()['data']):
		return "Error loading profile. Make sure profile is public and exists."
	else:
		user_id = int(user.json()['data'][0]['id'])

	# Make request for user info
	user_request = requests.get("https://api.instagram.com/v1/users/%s/?access_token=%s" % (user_id, creds.ACCESS_TOKEN))

	# Get user info as dict, used to populate
	user_info = user_request.json()['data']

	media_request = requests.get("https://api.instagram.com/v1/users/%s/media/recent/?access_token=%s&count=20" % (user_id, creds.ACCESS_TOKEN))

	likes = []
	comments = []
	days = []
	hours = []
	filters = []
	locations = []
	tags = []
	tag_positions = []

	for i in range(0, 20):
		likes.append(media_request.json()['data'][i]['likes']['count'])
		comments.append(media_request.json()['data'][i]['comments']['count'])
		days.append(datetime.datetime.fromtimestamp(int(media_request.json()['data'][i]['created_time'])).strftime('%a'))
		hours.append(datetime.datetime.fromtimestamp(int(media_request.json()['data'][i]['created_time'])).strftime('%H'))
		filters.append(media_request.json()['data'][i]['filter'])
		if not media_request.json()['data'][i]['location']:
			pass
		else:
			locations.append([media_request.json()['data'][i]['location']['latitude'], media_request.json()['data'][i]['location']['longitude']])
		for x in range(0, len(media_request.json()['data'][i]['users_in_photo'])):
			tags.append([media_request.json()['data'][i]['users_in_photo'][x]['user']['username'], media_request.json()['data'][i]['users_in_photo'][x]['user']['id']])
			tag_positions.append([media_request.json()['data'][i]['users_in_photo'][x]['position']['x'], media_request.json()['data'][i]['users_in_photo'][x]['position']['y']])

	all_data = {}
	all_data['likes'] = likes 
	all_data['comments'] = comments
	all_data['days'] = days
	all_data['hours'] = hours
	all_data['filters'] = filters
	all_data['locations'] = locations
	all_data['tags'] = tags
	all_data['tag_positions'] = tag_positions

	return json.dumps(all_data)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
