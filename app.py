#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Markup, request, render_template, redirect, url_for, flash
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json 
import time
import math
import datetime
import creds
import sys
import calendar

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.secret_key = creds.ACCESS_TOKEN

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/u/<user_input>', methods=['GET'])
def get_data(user_input):

	# fake user agent
	ua = UserAgent()
	header = {'User-Agent':str(ua.random)}

	# make requests
	user_request = requests.get("https://www.instagram.com/{}/".format(user_input.lower()), headers=header)
	user_soup = BeautifulSoup(user_request.text, 'html.parser')

	# case for incorrect username
	if len(user_soup.findAll('div', attrs={'class':'error-container'})) > 0:
		missingDataError("user does not exist.")

	# find json in page
	for src in user_soup.findAll('script'):
		if "window._sharedData" in src.text: 
			raw_json_src = src.text.replace("window._sharedData = ", "")[:-1]

			all_data = {}

			# load as json object
			json_src = json.loads(raw_json_src)

			raw_user_data = json_src['entry_data']['ProfilePage'][0]['graphql']['user']

			# case for private user
			if raw_user_data['is_private']:
				missingDataError("user is private")

			# catch if data is missing
			user_data = {
				"username" : raw_user_data['username'] if not None else missingDataError("could not load"),
				"followed_by" : raw_user_data['edge_followed_by']['count'] if not None else missingDataError("could not load"),
				"following" : raw_user_data['edge_follow']['count'] if not None else missingDataError("could not load"),
				"profile_picture" : raw_user_data['profile_pic_url'] if not None else missingDataError("could not load")
			}

			# weekdays list
			weekdays_count = []

			for wd in list(calendar.day_abbr):
				weekdays_count.append([wd, 0])

			# re-arrange for media counts
			weekdays_count.insert(0, weekdays_count[-1])
			weekdays_count.pop()

			# hours list
			hours_count = []

			for hr in range(0, 24):
				hours_count.append([str(hr), 0])

			# collect all media
			media_arr = []

			# max 12 media
			for med in raw_user_data['edge_owner_to_timeline_media']['edges']:
				media_dict = {
					"likes" : med['node']['edge_liked_by']['count'],
					"video" : med['node']['is_video'],
					"caption" : med['node']['edge_media_to_caption']['edges'][0]['node']['text'],
					"comments" : med['node']['edge_media_to_comment']['count'],
					"date" : datetime.datetime.fromtimestamp(med['node']['taken_at_timestamp']).strftime('%y/%m/%d'),
					"weekday" : datetime.datetime.fromtimestamp(med['node']['taken_at_timestamp']).strftime('%w'),
					"hour" : datetime.datetime.fromtimestamp(med['node']['taken_at_timestamp']).strftime('%-H')
				}
				media_arr.append(media_dict)

				weekdays_count[int(media_dict['weekday'])][1] += 1
				hours_count[int(media_dict['hour'])][1] += 1


			# zero pad hours
			for x in range(0, len(hours_count)):
				hours_count[x][0] = str(hours_count[x][0]).zfill(2)


			# make new data structure
			all_data['user_info'] = user_data
			all_data['media_info'] = media_arr
			all_data['weekdays_count'] = weekdays_count
			all_data['hours_count'] = hours_count

	return render_template('chart.html', all_data=all_data)

def missingDataError(msg):
	flash("Error loading profile: {}".format(msg))		
	return redirect(url_for("home"))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
