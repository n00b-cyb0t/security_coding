import requests

# "If you're using the InternetDB API to make money then you need an enterprise license." https://enterprise.shodan.io/

def openport(ip):
    result = []
    try:
        host = requests.get("https://internetdb.shodan.io/"+ip).json()
        result.append(host)

    except Exception as err: 
            print("Error: " + str(err))
    return result


result = openport("104.102.121.149")
print(result)
            
