from bs4 import BeautifulSoup
import urllib
#csv is for the csv writer
import csv

#initiates the dictionary to hold the output

holder = []

#this is the target URL
target_url = "targetchild.html"

data = []

def bodyscraper(url):
    #opens the url for read access
    this_url = urllib.urlopen(url).read()
    #creates a new BS holder based on the URL
    soup = BeautifulSoup(this_url, 'lxml')

    #finds the table
    table = soup.find('td', {'class':'b12c'})
    print table
    #zeros in on the element that contains the data that matters
    #two things match this criteria, you only want the second one
    #body_data = table.find('td', {'width':'650'})
    #print body_data

    data.append(table)

    holder.append(data)

bodyscraper(target_url)


with open('bodyscraper.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(holder)
