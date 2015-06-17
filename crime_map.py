import requests
import pygmaps
import math
import matplotlib.pyplot as plt


api_call = requests.get("https://data.seattle.gov/resource/7ais-f98f.json")

all_items = api_call.json()
otype = str("offense_type")
ocode = str("offense_code")

offenses = set()
offense_code = set()

for dict in all_items:
    keys = dict.keys()
    for key in keys:
        if str(key) == otype:
            offenses.add(dict.get(key))

# Violent crimes are as follows:
# RECKLESS BURNING
# ASSLT-AGG-POLICE-WEAPON
# ROBBERY-BUSINESS-GUN
# ASSLT-AGG-WEAPON
# ASSLT-AGG-GUN
# THREATS-KILL
# ROBBERY-STREET-BODYFORCE
# ROBBERY-STREET-WEAPON
# ASSLT-AGG-BODYFORCE
# ROBBERY-STREET-GUN

vkeys = ["RECKLESS BURNING", "ASSLT-AGG-POLICE-WEAPON", "ROBBERY-BUSINESS-GUN",
         "ASSLT-AGG-WEAPON", "ASSLT-AGG-GUN", "ROBBERY-STREET-BODYFORCE",
         "ROBBERY-STREET-WEAPON", "ASSLT-AGG-BODYFORCE", "THREATS-KILL",
         "ROBBERY-STREET-GUN"]

subSet = []
lat = []
lon = []
tags = []
diffLat = []
diffLon = []

for dict in all_items:
    for i in range(0, len(vkeys)):
        vals = dict.values()
        if unicode(vkeys[i], "utf-8") in vals:
            subSet.append(dict)

for dict in subSet:
    lat.append(float(dict[u'latitude']))
    lon.append(float(dict[u'longitude']))
    tags.append(str(dict[u'offense_type']))


center = [47.611730, -122.312223]
mymap = pygmaps.maps(center[0], center[1], 11)
for i in range(0, len(lat)):
    mymap.addpoint(float(lat[i]), float(lon[i]),"#FF0000")

mymap.draw('./crime_map.html') #open mymap.draw to view

minlat = float(min(lat))
minlon = float(min(lon))
for i in range(0, len(lat)):
    diffLat.append(math.fabs(lat[i]-minlat))
    diffLon.append(math.fabs(lon[i]-minlon))

plt.plot(diffLon, diffLat, color = "blue", marker = "o", linestyle = "")
plt.show()


from sklearn import cluster
import numpy as np

data = np.array([diffLon, diffLat]).transpose()
clusters = cluster.KMeans(n_clusters=4)
clusters.fit(data)
centers = clusters.cluster_centers_
colors = ['red', 'blue', 'green', 'yellow']
for i in range(0, len(lat)):
    plt.plot(diffLon, diffLat, color = colors[clusters.labels_[i]], marker = "o", linestyle = "")
plt.show()













