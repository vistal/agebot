import praw
from random import randint
import re
import os

posts = []
agedict = []

if os.path.isfile('posts.txt'):
	with open('posts.txt', 'r') as file:
		posts = [line.rstrip('\n') for line in file]

if os.path.isfile('agelist.txt'):
	agedict = open("agelist.txt").readlines()


def process_comment(comment):
	if "!age" in comment.body.lower() and "(" in comment.body.lower() and ")" in comment.body.lower():
		if comment.id not in posts:
#			match = re.search(r'!age (\w+)', comment.body, re.IGNORECASE)
			match = re.search(r'\((.*?)\)', comment.body, re.IGNORECASE)
			indices = [i for i, s in enumerate(agedict) if match.group(1).lower() in s.lower()]
			index = -1
			for i in indices:
				index = i
			if index == -1:
				comment.reply("No data on file")
			else:
				replydict = str.replace(agedict[index],',',' is')
				comment.reply("The legal drinking age in " + replydict)
			posts.append(comment.id)
			with open('posts.txt', 'w') as file:
				for item in posts:
					file.write('{}\n'.format(item))
		else:
			return

reddit = praw.Reddit('agebot')

for comment in reddit.subreddit('alcohol').stream.comments():
	process_comment(comment)
