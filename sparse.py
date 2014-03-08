import re
def sparse(d):
    r = []
    f = []
    e = d.splitlines()
    for i in e:
        if i[0:5] == "+CMGL":
            print i
            f.append(re.search("\+[0-9]{12}",i).group(0))
            
        else:
            f.append(i)
            print f
            r.append(f)
            f = []

    return r
