import time, json, os

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

output = {}


for k in J["Sent"]:
    obj = J["Sent"][k]

    date = obj["Created"].split(" ")[0]
    if not date in output:
        output[date] = [0, 0]
    output[date][0] += 1

for k in J["Received"]:
    obj = J["Received"][k]

    date = obj["Created"].split(" ")[0]
    if not date in output:
        output[date] = [0, 0]
    output[date][1] += 1

print "Data days", len(output)

template = template.replace("{INPUT_DATA}", json.dumps(output))

fo = open(output_file, "w+")
fo.write(template)
fo.close()

print "Done"
