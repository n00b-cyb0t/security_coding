import nmap
import json

# this script needs to be run as root for certain arguements to work properly

nm = nmap.PortScanner()

def manualscan(ip, args):
    result = [] 
    try: 

        s = nm.scan(hosts=ip, arguments=args)
        result.append(s)

    except Exception as e: 
        print("error: "+ str(e))
    return result


result = manualscan('192.168.0.1', '-sV -sS -p 21,22,80,443,137,139,3389')
data = {"nmap_results": result}
print(json.dumps(data, indent=3))
