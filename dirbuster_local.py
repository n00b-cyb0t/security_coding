from urllib import request
import requests 

directories = []

with open(r'C:\users\user\desktop\directory-list-2.3-medium.txt') as f:
    lines = f.read()
    directories += lines.split("\n")
#print(directories)

def buster(url):

    for x in directories:
        print("Trying directory: " +str(x))
        g = requests.get(url+"/"+x)
        print("Status Code: " + (str(g.status_code)))
        print("Content: " + str((g.content)))
        print("\n")

buster("http://10.0.0.1")
