from ast import arg
from re import X
from stat import S_IFPORT
import requests
import shodan 


def shodan_network(key, shodan_filter, company):
    api = shodan.Shodan(key)

    # different filter types can be found at: https://beta.shodan.io/search/filters

    #lookup host by IP
    #s_ip = api.host(ip)

    #query language 
    s_query = api.search(shodan_filter+":"+'"'+company+'"' )

    count = 0
    
    for x in s_query['matches']:
        try: 
            count+=1
            host = x['http']['host']
            robots = x['http']['robots']
            http_status = x['http']['status']
            http_redirects = x['http']['redirects']
            http_server = x['http']['server']
            sitemap = x['http']['sitemap']
            org = x['org']
            asn = x['asn']
            isp = x['isp']
            port = x['port']
            ssl_versions = x['ssl']['versions']
            ssl_issuedate= x['ssl']['cert']['issued']
            ssl_expiredate = x['ssl']['cert']['expires']
            ssl_expired = x['ssl']['cert']['expired']
            ssl_cipher = x['ssl']['cipher']
            location = x['location']
            ssl_hostnames = x['hostnames']

            print("--------------------")
            print("host: " + str(x['http']['host']))
            print("robots: " + str(x['http']['robots']))
            print("HTTP status: " + str(x['http']['status']))
            print("HTTP redirects: " + str(x['http']['redirects']))
            print("Server: " + str(x['http']['server']))
            print("sitemap: " + str(x['http']['sitemap']))
            print("org: " + str(x['org']))
            print("ASN: " + str(x['asn']))
            print("ISP: " + str(x['isp']))
            print("Port: " + str(x['port']))
            print("SSL Versions: " + str(x['ssl']['versions']))
            print("SSL Issued Date: " + str(x['ssl']['cert']['issued']))
            print("SSL Exp Date: " + str(x['ssl']['cert']['expires']))
            print("SSL Expired?: " + str(x['ssl']['cert']['expired']))
            print("SSL Ciphers: " + str(x['ssl']['cipher']))
            print("SSL Hostnames: " + str(x['hostnames']))
            print("Location: " + str(x['location']))
            print("--------------------")
            print('\n')
   

        except KeyError as err: 
            print("Key not found: " + str(err))
            continue
        
    print("Number of returned results: "+ str(count))
        

    # shodan scan
    #s_scan = api.scan(ip)

    # use scan id from above to get the status
    #s_status = api.scan_status("3g81M2WpnUmC3c98")

    #rint(api.search_facets())

shodan_query = shodan_network("api_key_here", "all", "navyfederal")
print(shodan_query)