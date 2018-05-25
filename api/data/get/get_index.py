from bs4 import BeautifulSoup
from  urllib.request import urlopen 

fname = "index.txt"
o = open(fname, 'w')



for i in range(1, 130):
    print ("Processing Serial: ", i)
    content = ""
    npages = ""
    tokens = ""

    sid = '%03d' % i
    url = "https://ehistory.osu.edu/books/official-records/"+str(sid)+"/"

    source = urlopen(url).read()
    soup = BeautifulSoup(source, 'html.parser')

    if ("Books" in soup.title.string):
        print ("Skipping serial: ", i) #doesn't exist
        continue

    content = soup.select('li.leaf.last')[0].text

    tokens = content.split(' ')
    for count, t in enumerate(tokens):
        if "Page" in t:
            npages = tokens[count + 1]
    print (i, npages, file=o)

