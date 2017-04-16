from bs4 import BeautifulSoup
import urllib
#csv is for the csv writer
import csv

#initiates the dictionary to hold the output

holder = []

#***********************************#
#***********************************#
#***CHANGE THE TARGET URL***********#
#***********************************#
#***AND NAME OF OUTPUT CSV FILE*****#
#***********************************#
#***********************************#


#this is the target URL
target_url = "http://sousuo.gov.cn/s.htm?q=&n=80&p=&t=paper&advance=true&title=&content=&puborg=&pcodeJiguan=%E5%9B%BD%E5%8F%91&pcodeYear=2016&pcodeNum=&childtype=&subchildtype=&filetype=&timetype=timeqb&mintime=&maxtime=&sort=pubtime&nocorrect=&sortType=1"

csv_name = "guofa-scraper-phase-three-output.csv"

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

#fills in the category (you need to go to the child page)
def scraper2(row):

    #variable to identify the row in holder
    g = holder[row]
    #the url is in spot [1] of the row
    url = g[1]

    #opens the url for read access
    this_url = urllib.urlopen(url).read()
    #creates a new BS holder based on the URL
    soup = BeautifulSoup(this_url, 'lxml')

    data = []

    #finds the table
    table = soup.find('tbody')
    #zeros in on the element that contains the data that matters
    #two things match this criteria, you only want the second one
    table_data = table.find_all('td', {'width':'360'})

    #this section is because some of the pages have a
    #width of 260 instead of 360

    if len(table_data) > 0:

        #let's just keep the second thing becusae  that's all that matters
        for element in table_data:
            #pulls just the text
            element_cleaned = element.text.encode('utf-8')
            #adds it to data
            data.append(element_cleaned)

    elif len(table_data) == 0:
        table_data_short = table.find_all('td', {'width':'260'})
        for element in table_data_short:
            #pulls just the text
            element_cleaned = element.text.encode('utf-8')
            #adds it to data
            data.append(element_cleaned)

    else:
        print "error"



    #the 2 has to be a variable
    holder[row].append(data[1])

    print "added category for row %s of %s" % ((row+1), len(holder))

#scrapes the body of the child page and outputs a html doc based on the content
def bodyscraper(row):

    #variable to identify the row in holder
    g = holder[row]
    #the url is in spot [1] of the row
    url = g[1]
    #the name of the doc is in spot [2] of the row
    docname = g[2]


    data = []


    #names the file based on the name of the document
    filename = docname+".html"
    target = open(filename, 'w')

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
    holder[row].append(data)

    print "created html for row %s of %s" % ((row+1), len(holder))

scraper(target_url)

#run scraper2 for each row in holder
scraper2_row_counter = 0
while scraper2_row_counter < len(holder):
    scraper2(scraper2_row_counter)
    scraper2_row_counter += 1

#outputs holder to a csv
#this is before the bodyscraper because the CSV should not have the HTML field
#if you want the csv to have the HTML field at some point just move it
#to the end

with open(csv_name, 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(holder)

#run bodyscraper for each row in holder
bodyscraper_row_counter = 0
while bodyscraper_row_counter < len(holder):
    bodyscraper(bodyscraper_row_counter)
    bodyscraper_row_counter += 1
