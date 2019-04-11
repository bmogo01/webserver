import datetime
import requests
import hashlib

superheroName = input("Name a Marvel Superhero: ")

public = '1e80bd38e6ee25f515f66c6e66da54f1'
private = '90756ba32da3cad5c2ac2b947ac95f18affb4d9c'
ts = datetime.datetime.now().timestamp()

input = str(ts)+private+public
hash = hashlib.md5(input.encode('ascii')).hexdigest()

query = "https://gateway.marvel.com:443/v1/public/characters?"
query += "name=%s" %superheroName
query += "&limit=100"
#query += "&offset=50"
query += "&apikey=%s" %public
query += "&hash=%s" %hash
query += "&ts=%s" %ts

#print("public: %s, ts: %s, hash: %s " % (public, ts, hash))
resp = requests.get(query)
print("Super hero description: ")
vals = resp.json()

try:
    print(vals["data"]["results"][0]["description"])
except IndexError:
    print("Sorry %s is not a character in the Marvel Universe" %superheroName)
