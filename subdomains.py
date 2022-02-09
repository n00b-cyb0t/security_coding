import sublist3r 

global sd
sd = []

global d
d = {}


def subd(sdomain):

    # each of the following fields is required in sublist3r
    subdomains = sublist3r.main(sdomain, 10, 'required.txt', ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
    for x in subdomains:
        sd.append(x)


d = {"subdomains": sd}

subd("navyfederal.org")
print(d)

