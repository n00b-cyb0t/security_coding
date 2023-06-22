from pickle import FALSE
from xml.dom import xmlbuilder
import requests
from bs4 import BeautifulSoup
import pandas as pd 

address = "10.0.0."


def scanheaders(ip):
    output = []
    j2 = dict()
    j2['IP'] = ip
    print("----------------")
    url = "https://securityheaders.com/?q=https%3A%2F%2F"+ip+"&followRedirects=on"
    r = requests.get(url, verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')

    status = str(r.status_code)

    if status != str(200):
        print("Scan not working, http status is: " + str(status))
    else:

        sorry = soup.select('h1')
        pills = soup.select('li')

        for x in sorry:
            if "Sorry" in x.text: 
                print("IP: " +ip+ " not scannable")
                j2['Scannable'] = "False"
                break
            else:

                try:
                    score = soup.select_one('.score').text
                    j2['Site Score'] = str(score)
                except Exception as e:
                    #print("exception: ", e)
                    pass
                
                for x in pills:
                    if "pill-red" in str(x) or "pill-orange" in str(x):
                        
                        o = x.text
                        output.append(o)
                j2['Missing Headers'] = output        
        return j2

for x in range(1,255):
    new = address+str(x)
    d = scanheaders(new)
    headers = pd.DataFrame(data=d)
    headers.to_csv(r"C:\Users\user\Desktop\test.csv")
    print(headers)

