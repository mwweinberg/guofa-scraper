from bs4 import BeautifulSoup
import urllib
#csv is for the csv writer
import csv

#initiates the dictionary to hold the output

holder = []

#this is the target URL
target_url = "target.html"

def scraper(url):

    #opens the url for read access
    this_url = urllib.urlopen(url).read()
    #creates a new BS holder based on the URL
    soup = BeautifulSoup(this_url, 'lxml')

    #finds all of the titles
    doc_title = soup.find_all('h3')

    #creates a list called mini holder
    mini_holder = []

    #for each of the titles
    for element in doc_title:

        #print element

        #this gets just the text of the element
        text = element.text.encode('utf-8')
        print text

        #this gets just the url of the element
        #by finding the thing tagged with 'a' and then pulling the 'href'
        doc_url = element.find('a').attrs['href']
        print doc_url


        #bundles the output of each round as a list
        mini_holder = [text, doc_url]
        #adds that list to the larger list
        holder.append(mini_holder)





scraper(target_url)

#outputs holder to a csv

with open('output.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(holder)
