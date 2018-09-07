import time, json, os, datetime

output = "data/output.json"

def parse_ts(s):
    return time.mktime(
        datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple())


files = []

for file in os.walk("data/"):
    #print file[0]
    for f in file:
        if "snap_history.json" in f:
            path = str(file[0]) + "/snap_history.json"
            files.append(path)


data_received = {}
data_sent = {}

for file in files:
    print "Reading ", file, len(data_received)

    f = open(file)
    data = json.loads( f.read() )
    for i in data["Received Snap History"]:
        #print i
        key = None
        if "Sender" in i:
            key = i["Recipient"] + i["Sender"] + i["Created"]
        else:
            key = i["From"] + i["Created"]

        i["ts"] = parse_ts(i["Created"].replace(" UTC",""))

        data_received[key] = i

    for i in data["Sent Snap History"]:
        #print i
        key = None
        if "Sender" in i:
            key = i["Recipient"] + i["Sender"] + i["Created"]
        else:
            key = i["To"] + i["Created"]

        i["ts"] = parse_ts(i["Created"].replace(" UTC",""))

        data_sent[key] = i

data = {
    "Sent": data_sent,
    "Received": data_received
}

open(output,"w+").write( json.dumps(data))
