#import dnspython
import dns.resolver
import json

def addrlookup(hosts, atype):
    # Types you can use are A, AAAA, MX, NS, PTR, TXT, etc

    result = []
    
    try:
        resolver = dns.resolver.resolve(hosts, atype)
        for x in resolver:
            x = x.to_text()
            result.append(x)
            #print(result)

    except Exception as e:
        print("resolver issue: " + str(e))

    return result



print('IP Address(s): ')
results = addrlookup("navyfederal.org", "A")
addresses = {"IPv4_addresses": results}
print(json.dumps(addresses, indent=3))

print("mail server(s): ")
results = addrlookup("navyfederal.org", "MX")
addresses2 = {"MX_addresses": results}
print(json.dumps(addresses2, indent=3))

print("name server(s): ")
results = addrlookup("navyfederal.org", "NS")
addresses3 = {"NS_addresses": results}
print(json.dumps(addresses3, indent=3))
