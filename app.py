#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Markup, request, render_template, redirect, url_for, flash
import requests
from bs4 import BeautifulSoup
import json 
import time
import math
import datetime
import sys
import calendar
import os
from pprint import pprint

app = Flask(__name__)
app.secret_key = (os.environ.get('secret_key'))

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/u/<user_input>', methods=['GET'])
def get_data(user_input):

	try:
		# make requests
		user_request = requests.get("https://www.instagram.com/{}/".format(user_input.lower()))
		user_soup = BeautifulSoup(user_request.text, 'html.parser')

		# case for incorrect username
		if len(user_soup.findAll('div', attrs={'class':'error-container'})) > 0:
			flash("Error loading profile: user does not exist")
			return redirect(url_for("home"))

		all_data = {}

		# find json in page
		for src in user_soup.findAll('script'):
			if "window._sharedData" in src.text: 
				raw_json_src = src.text.replace("window._sharedData = ", "")[:-1]

				# load as json object
				json_src = json.loads(raw_json_src)

				raw_user_data = json_src['entry_data']['ProfilePage'][0]['graphql']['user']

				# case for private user
				if raw_user_data['is_private']:
					flash("Error loading profile: user is private")
					return redirect(url_for("home"))

				# catch if data is missing
				try:
					user_data = {
						"username" : raw_user_data['username'],
						"followed_by" : raw_user_data['edge_followed_by']['count'],
						"following" : raw_user_data['edge_follow']['count'],
						"profile_picture" : raw_user_data['profile_pic_url']
					}

				except KeyError:
					flash("Error loading profile.")
					return redirect(url_for("home"))

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

				break

		return render_template('chart.html', all_data=all_data)

	except Exception as e:
		print(e)
		flash("Something went wrong!")
		return redirect(url_for("home"))


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
