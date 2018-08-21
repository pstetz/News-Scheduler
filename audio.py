# Removes warnings that occassionally show in imports
import warnings
warnings.filterwarnings('ignore')

import re
import os
import time
import glob

# Libraries for website scraping
from bs4 import BeautifulSoup
import requests
import urllib

def url_valid(url):
	"""
	Returns a boolean value checking if the url is valid

	The motivation is to see if the new program has been uploaded
	"""
	
	request = requests.get(url)
	return request.status_code == 200

def get_audio_url(url):
	"""
	Finds the audio url given a PBS Newshour page
	"""
	page = urllib.request.urlopen(url)
	page = BeautifulSoup(page)

	audio = page.find_all(text=re.compile('Listen to the Broadcast'))
	assert len(audio) == 1

	audio = [s.parent.parent.parent for s in audio]
	audio = audio[0]

	audio_url = audio.find("source")["src"]
	return audio_url

def replace_audio(url, header):
	today = time.strftime("%Y-%m-%d")
	page = urllib.request.urlopen(url)
	directory = os.path.expanduser('~') + "/Desktop"
	new_filename = f"{header}_{today}.mp3"
	with open(f"{directory}/{new_filename}", "wb") as output:
		output.write(page.read())
		delete_old_audio(new_filename, header, directory)

def delete_old_audio(new_filename, header, directory):
	files = glob.glob(directory + "/*")
	for filename in files:
		if os.path.isdir(filename):
			continue
		filename = filename.split("/")[-1]
		print(filename)
		if header in filename and filename != new_filename:	
			os.remove(f"{directory}/{filename}")


if __name__ == "__main__":
	url = "https://www.pbs.org/newshour/show/august-20-2018-pbs-newshour-full-episode"
	if url_valid(url):
		audio_url = get_audio_url(url)
		replace_audio(audio_url, "PBS_Newshour")

print("Finished")
