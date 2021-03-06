from bs4 import BeautifulSoup
import urllib
#csv is for the csv writer
import csv

#initiates the dictionary to hold the output

holder = []

#this is the target URL
target_url = "http://sousuo.gov.cn/s.htm?q=&n=80&p=&t=paper&advance=true&title=&content=&puborg=&pcodeJiguan=%E5%9B%BD%E5%8F%91&pcodeYear=2016&pcodeNum=&childtype=&subchildtype=&filetype=&timetype=timeqb&mintime=&maxtime=&sort=pubtime&nocorrect=&sortType=1"

def scraper(url):

    #opens the url for read access
    this_url = urllib.urlopen(url).read()
    #creates a new BS holder based on the URL
    soup = BeautifulSoup(this_url, 'lxml')

    #***********************************#
    #******TITLE SECTION****************#
    #***********************************#

    #finds all of the titles
    doc_title = soup.find_all('h3')

    #creates a list called title mini holder
    title_mini_holder = []

    #for each of the titles
    for element in doc_title:

        #print element

        #this gets just the text of the element
        text = element.text.encode('utf-8')
        #print text

        #this gets just the url of the element
        #by finding the thing tagged with 'a' and then pulling the 'href'
        doc_url = element.find('a').attrs['href']
        #print doc_url


        #bundles the output of each round as a list
        title_mini_holder = [text, doc_url]
        #adds that list to the larger list
        holder.append(title_mini_holder)

    #***********************************#
    #******EVERYTHING ELSE SECTION****************#
    #***********************************#

    #finds the doc numbers, promilgation date, and interet release date
    #which are in <span class="sp">
    #this will end up with all three values over and over
    #that means that you will need to chunk them into threes
    other_elements = soup.find_all('span', {'class':'sp'})

    #creates a list called number mini holder
    values_mini_holder = []

    #for each of the numbers
    for element in other_elements:

        #pulls the text of each element
        text = element.text.encode('utf-8')

        #adds teh element to values_mini_holder
        values_mini_holder.append(text)

    #these variables allow matching between the title/URL and the other data

    #this keeps track of the document (we have the title and URL already)
    holder_spot_counter = 0
    #this keeps track of three new elements (doc num, prom date, release date)
    #since these are in chunks of three it needs to have its own variable
    other_three_counter = 0

    #this adds the three relevant values to the existing title/url
    while holder_spot_counter < len(holder):

        #the goal here is to add doc num, prom date, and release date
        #so for each existing spot you need to move three steps through values_mini_holder

        #for example the first doc (holder[0]) needs
        #the values_mini_holder[0], values_mini_holder[1], & values_mini_holder[2]

        #then holder[1] needs
        #values_mini_holder[3], values_mini_holder[4], values_mini_holder[5]


        holder[holder_spot_counter].append(values_mini_holder[other_three_counter])
        holder[holder_spot_counter].append(values_mini_holder[other_three_counter+1])
        holder[holder_spot_counter].append(values_mini_holder[other_three_counter+2])

        holder_spot_counter += 1
        other_three_counter += 3




scraper(target_url)

#outputs holder to a csv

with open('guofa-scraper-phase-one-output.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(holder)
