from bs4 import BeautifulSoup
from  urllib.request import urlopen 


## for serial 1 to 129 
url = "https://ehistory.osu.edu/books/official-records/007/"
for i in range(1, 946):
    page = '%04d' % i
    fname = "./07/" + str(i) + ".txt"
    o = open(fname, 'w')
    print (i)

    fullurl = url + page
    source = urlopen(fullurl).read()
    text = ""

    soup = BeautifulSoup(source, 'html.parser')
    content = soup.find("blockquote").find_all("p")
    for p in content:
        text = text + p.text
    print (text, file=o)

