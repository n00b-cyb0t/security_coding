import sublist3r 
import json

def subd(sdomain):
    results = []
    try:
        subdomains = sublist3r.main(sdomain, 10, 'required.txt', ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
        for x in subdomains:
            results.append(x)
    except Exception as e:
        print("subd: " + str(e))
    return results



results = subd("domain.org")
d = {"subdomains": results}
print(json.dumps(d, indent=3))

