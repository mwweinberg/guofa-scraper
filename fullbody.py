from bs4 import BeautifulSoup
import urllib
#csv is for the csv writer
import csv

#initiates the dictionary to hold the output

holder = []

#this is the target URL
target_url = "http://www.gov.cn/zhengce/content/2016-12/02/content_5142197.htm"

data = []

filename = "fullbody.html"
target = open(filename, 'w')

def bodyscraper(url):
    #writest the header for the html file so that the browser decodes chinese
    target.write('<meta charset="utf-8"/>')

    #opens the url for read access
    this_url = urllib.urlopen(url).read()
    #creates a new BS holder based on the URL
    soup = BeautifulSoup(this_url.decode("utf-8"), 'lxml')
    #finds the body text
    body = soup.find('td', {'class':'b12c'})
    #write the whole decoded body to html directly
    target.write("%s\n" % body)

    #appends the body to the data list
    data.append(body)
    #appends the data list to the holder list
    holder.append(data)





bodyscraper(target_url)


with open('bodyscraper.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(holder)
