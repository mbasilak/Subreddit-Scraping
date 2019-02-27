import praw
import urllib

reddit = praw.Reddit(client_id='APP CLIENT_ID', \
                     client_secret='APP CLIENT_SECRET CODE', \
                     user_agent='YOUR REDDIT APP NAME', \
                     username='YOUR REDDIT USERNAME', \
                     password='YOUR PASSWORD')

subreddit = 'Any Subreddit without r/'

redChar = [' ','{','}','\'','\\n','"created_utc"','"data"',':','[',']']


#Getting the timestamp of first post on the subreddit

ps = urllib.request.urlopen("https://api.pushshift.io/reddit/submission/search/?subreddit="+subreddit+"&sort=asc&filter=created_utc&size=1")
htmltext = ps.read()
htmltext = str(htmltext)
htmltext = htmltext[1:]
for c in redChar:
    htmltext = htmltext.replace(c,'')
firstPostTimestamp = int(htmltext)


#Getting the timestamp of last post on the subreddit

ps = urllib.request.urlopen("https://api.pushshift.io/reddit/submission/search/?subreddit="+subreddit+"&sort=desc&filter=created_utc&size=1")
htmltext = ps.read()
htmltext = str(htmltext)
htmltext = htmltext[1:]
for c in redChar:
    htmltext = htmltext.replace(c,'')
lastPostTimestamp = int(htmltext)


#Getting the timestamp of every thousandth post

Timestamp = firstPostTimestamp-100 
times = [] #list of every thousandth post's timestamp
while Timestamp < lastPostTimestamp:
    times.append(Timestamp)
    ps = urllib.request.urlopen("https://api.pushshift.io/reddit/submission/search/?subreddit="+subreddit+"&sort=asc&filter=created_utc&after="+str(Timestamp)+"&size=1000")
    htmltext = ps.read()
    htmltext = str(htmltext)
    htmltext = htmltext[1:]
    for c in redChar:
        htmltext = htmltext.replace(c,'')
    array = htmltext.split(',')
    Timestamp = int(array[-1])
    percentage = (Timestamp-firstPostTimestamp)/(lastPostTimestamp-firstPostTimestamp)*100
    print(str(round(percentage,2))+'%',end='\r') 
"""
Percentage is calculated based on the timestamp.
Therefore change in percentage would be high when total submission per week is low.
So it is probable that change in percentage would be high in the beginning and low towards the end.
"""

#Getting the list of every post's ID

redChar = [' ','{','}','\'','\\n','"id"','"data"',':','[',']','"']
idList = []
for Timestamp in times:
    ps = urllib.request.urlopen("https://api.pushshift.io/reddit/submission/search/?subreddit="+subreddit+"&sort=asc&filter=id&after="+str(Timestamp)+"&size=1000")
    htmltext = ps.read()
    htmltext = str(htmltext)
    htmltext = htmltext[1:]
    for c in redChar:
        htmltext = htmltext.replace(c,'')
    idList = idList + htmltext.split(',')
    percentage = (Timestamp-firstPostTimestamp)/(lastPostTimestamp-firstPostTimestamp)*100
    print(str(round(percentage,2))+'%',end='\r')
print(str(round(100.00,2))+'%',end='\r')


# Getting the List of every submission

submissionList = []
current = 0
totalSubmissions = len(idList)
for ID in idList:
    submissionList.append(reddit.submission(id=ID))
    current += 1
    percentage = current/totalSubmissions*100
    print(str(round(percentage,2))+'%',end='\r')

"""
You will get every post submitted in the subreddit by iterating through SubmissionList
"""
