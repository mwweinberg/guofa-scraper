guofa-scraper.py is the current stable version and is everything you need.  Remember to change the URL and csv output name in the script before running it!



alt_simple_doctitle.py - (stable) works to pull doc title and URL and put them into a CSV 

alt_simple_fiveelements.py - (stable) outputs all five elements of each doc into a CSV. This is a functioning version of phase 1

goufa-scraper-phase-one.py - identical to alt_simple_fiveelements but with the real URL. Takes the URL and outputs a CSV with all five elements of each doc.

guofa-scraper-phase-two.py - Takes the URL and outputs a CSV with all five elements on the primary page and then goes to the child pages and adds the category.

guofa-scraper-phase-three.py - Does everything - fills in the CSV with all five elments and outputs HTML documents for each document in the folder where it was run.  Was converted into gofa-scraper.py.

fullbody.py - takes the body text of the doc and puts it into a CSV and outputs it into an HTML document
