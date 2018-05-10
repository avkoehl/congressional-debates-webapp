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


    ## for each serial, get data from each page
    for i in range(npages + 1):
        page = '%04d' % i
        ofile = open(odir + str(i) + ".txt", "w")
        text = "" 

        print ("page: ", page)

        fullurl = url + page
        source = urlopen(fullurl).read()

        soup = BeautifulSoup(source, 'html.parser')
        content = soup.find("blockquote").find_all("p")
        for p in content:
            text = text + p.text

        print (text, file=ofile)

