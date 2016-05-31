#! /usr/bin/python

import twitter_pb2
import sys
import re
import csv
import copy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import stem
from collections import defaultdict

# Define three functions that describe the raw data, cleaned data, and 
# cleaned data respectively:

def getModels(twitter):
# identify the models in this set of tweets and get a count 
# of the number of tweets per model 
	modelBank = {}
	for tweet in twitter.tweets:	
		strTweet = str(tweet.insert.model)
		if strTweet in modelBank:
			modelBank[strTweet] += 1
		else: 
			modelBank[strTweet] = 1
	return modelBank.keys()

def modelWords(models, textBank):
# Get the most frequent words associated with each model
	stopset = set(stopwords.words('english'))
	for model in models:
		# preprocess the text data by removing urls, @user, various punctuation,
		# numbers (which were typically associated to the model number, release year, or other 
		# potentially less relevant information) and single characters
		textBank[model] = re.sub("(\@|http.?\://)\S+", '', textBank[model], flags=re.MULTILINE)
		textBank[model] = re.sub("[\'\/\)\(;,?!#@$%^&*\+~\[\]:\.\|-]", '', textBank[model], flags=re.MULTILINE)
		textBank[model] = re.sub("[0-9]", '', textBank[model], flags=re.MULTILINE)
		textBank[model] = re.sub(" [A-Za-z] ", '', textBank[model], flags=re.MULTILINE)
	
		# tokenize, set to lowercase, check to make sure words are note in dictionary of 
		# stopwords, then stem
		tokens = word_tokenize(textBank[model].lower())
	 	tokens = [w for w in tokens if not w in stopset]
		pt = stem.PorterStemmer() # use least aggressive stemmer available
		tokens = [pt.stem(i) for i in tokens]	

		# count the frequency of the remaining word stems, report top 20 frequencies in 
		# descending order
		keyWords = {}
		for word in tokens:	
			word = str(word)
			if word in keyWords:
				keyWords[word] += 1
			else: 
				keyWords[word] = 1

		sortedKW = sorted(keyWords, key = keyWords.get)
		sortedKW.reverse()
		sortedValues = sorted(keyWords.values())
		sortedValues.reverse()
		print model
		print("Top 15 associated words: " + str(sortedKW[:15]))
		print("With numbers of instances: " + str(sortedValues[:15]))

def organicTweets(models,cleanTweet):
# Rank models according to "organic" nature of tweets. To do this, create a ratio of inorganic/total
# tweets. Inorganic tweets are determined by: having key phrases in the text portion of the tweet
# or by having the word "news" in their user id
	organic = {}
	inorganicBank = ["prices start at", "launch on", "rs.", "for sale", "arrives in", "exclusive:"]
	for model in models:
		nTweets = len(cleanTweet[model])
		organicTweets = 0.0
		for uname in cleanTweet[model]:
			inorg = 0
			# do not deal with tweets where the user id has unicode characters
			# no penalty for these users, but do not consider the tweet organic either
			try:
				f = open('/dev/null', 'w')
				sys.stdout = f
				print uname[0]
				sys.stdout = sys.__stdout__	
			except UnicodeEncodeError:
				nTweets -= 1
				continue

			if "news" in uname[0].lower():
				continue

			for iorg in inorganicBank:
				lt = uname[1].lower()
				if iorg in lt:
					inorg = 1
					break
			if inorg == 1:
				continue

			organicTweets += 1
		organic[model] = organicTweets/nTweets
	
	sys.stdout = sys.__stdout__
	sortedKW = sorted(organic, key = organic.get)
	sortedKW.reverse()
	sortedValues = sorted(organic.values())
	sortedValues.reverse()

	print(str(sortedKW))
	print(str(sortedValues))

# Main body, read in protocol buffer, preprocess tweets to discard spam and then call functions
# to get aggregate information about the data
twitter = twitter_pb2.Tweets()

file = open("twitter.pb", "rb")
twitter.ParseFromString(file.read())
file.close()

# identify the models in this set of tweets
models = getModels(twitter)
# remove "TVS Company General" as it is not a model
models.remove("TVS Company General")

# create two dictionaries, textBank to hold the text of every relevant tweet
# body per model and cleanTweet to hold a tuple of (user name, text) per model
textBank = {}
for model in models:
	textBank[model] = ''

cleanTweet= defaultdict(list)
  
# Spam bank, some words commonly associated with spam (or not motorcycles in the
# dataset)
spamBank = ['bid now!','samsung','iphone','free','click','nvidia']

# Loop through all tweets, skip tweets that have unicode in the body and those that
# have been identified as spam. Note unicode is identified by trying to print text,
# to avoid actual printing, output is turned off (sys.stdout = f) and then set back
# to default at a later time (sys.stdout = sys.__stdout__)
for tweet in twitter.tweets:
	spam = 0
	organic = 0
	if "TVS Company General" in str(tweet.insert.model):
		continue
	try:
		f = open('/dev/null', 'w')
		sys.stdout = f
		print tweet.insert.text
		sys.stdout = sys.__stdout__	
	except UnicodeEncodeError:
		continue

	for sb in spamBank:
		lt = tweet.insert.text.lower()
		if sb in lt:
			spam = 1
			break
	if spam == 1:
		continue

	textBank[tweet.insert.model]=textBank[tweet.insert.model]+" "+ tweet.insert.text
	cleanTweet[tweet.insert.model].append((tweet.insert.u_name,tweet.insert.text))

sys.stdout = sys.__stdout__	

# Print most frequent words associated with each model
modelWords(models, textBank)

# Rank models according to "organic" nature of tweets
organicTweets(models, cleanTweet)



