from bs4 import BeautifulSoup
from  urllib.request import urlopen 
import pathlib

indexfile = open("index.txt")

## get the serial number and and number of pages
for line in indexfile:
    elements = line.split(' ')
    serial = '%03d' % int(elements[0])
    npages = int(elements[1])

    print ("Processing serial: ", serial)

    url = "https://ehistory.osu.edu/books/official-records/" + serial + "/"
    odir = "./" + serial + "/"
    pathlib.Path(odir).mkdir(parents=True, exist_ok=True) 

    if int(serial) < 122:
        print ("already done ... moving on")
        continue


    ## for each serial, get data from each page
    for i in range(npages + 1):
        page = '%04d' % i
        ofile = open(odir + str(i) + ".txt", "w")
        text = "" 

        print ("page: ", page)

        fullurl = url + page
        source = urlopen(fullurl).read()

        soup = BeautifulSoup(source, 'html.parser')
        if ("Books" in soup.title.string):
            print ("skipping page", i) # doesn't exist
            continue

        if (soup.find("blockquote")):
            content = soup.find("blockquote").find_all("p")
            for p in content:
                text = text + p.text

        else:
            print ("no text found")

        print (text, file=ofile)

