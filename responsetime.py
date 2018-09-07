#
#   responsetime.py
#   Calculates average responsetime for sent & received snaps
#

import time, json, os, datetime
from dateutil.parser import parse

template_file = "templates/template-1.html"
data_file = "data/output.json"
output_file = "data/output-chart.html"

f = open(template_file)
template = f.read()
f.close()


df = open(data_file)
data = df.read()
df.close()

J = json.loads( data )

combinedList = []

for k in J["Sent"]:
    obj = J["Sent"][k]
    obj["type"] = "sent"
    if not "To" in obj:
        obj["To"] = obj["Recipient"]
    combinedList.append( obj )

for k in J["Received"]:
    obj = J["Received"][k]
    obj["type"] = "received"
    if not "From" in obj:
        obj["From"] = obj["Sender"]

    combinedList.append( obj )


print "Combined list, total items:", len(combinedList)
print "Sorting it..."

#sortedList = []

combinedList.sort(key=lambda snap: snap["ts"])

#   Average response time by SENT snaps

sent_snaps = {}

#   username

replies = []
replies_users = {}

for snap in combinedList:

    if snap["type"] == "sent":
        #print snap
        sent_snaps[ snap["To"] ] = {"time": snap["ts"]}

    if snap["type"] == "received":
        username = snap["From"]
        if username in sent_snaps:
            took = snap["ts"] - sent_snaps[ username ]["time"]
            if took < 86400:
                replies.append({"username": username, "time": took})
                if not username in replies_users:
                    replies_users[username] = []
                replies_users[username].append({"time": took})



print "Replies", len(replies)
total = 0
for reply in replies:
    total += reply["time"]

print "Average", (float(total)/len(replies))

user_list = []

for user in replies_users:
    list = replies_users[user]
    items = len(list)
    total = 0
    for item in list:
        total += item["time"]
    avg = total / float(items)

    user_list.append({"user": user, "avg": avg})


user_list.sort(key=lambda reply: reply["avg"])

for user in user_list[:20]:
    print user["user"], " "*(20-len(user)),user["avg"]


print ".........."


received_snaps = {}

#   username

replies = []
replies_users = {}

for snap in combinedList:

    if snap["type"] == "received":
        #print snap
        received_snaps[ snap["From"] ] = {"time": snap["ts"]}

    if snap["type"] == "sent":
        username = snap["To"]
        if username in received_snaps:
            took = snap["ts"] - received_snaps[ username ]["time"]
            if took < 86400:
                replies.append({"username": username, "time": took})
                if not username in replies_users:
                    replies_users[username] = []
                replies_users[username].append({"time": took})



print "Replies", len(replies)
total = 0
for reply in replies:
    total += reply["time"]

print "Average", (float(total)/len(replies))

user_list = []

for user in replies_users:
    list = replies_users[user]
    items = len(list)
    total = 0
    for item in list:
        total += item["time"]
    avg = total / float(items)

    user_list.append({"user": user, "avg": avg})


user_list.sort(key=lambda reply: reply["avg"])

for user in user_list[:20]:
    print user["user"], " "*(20-len(user)),user["avg"]
