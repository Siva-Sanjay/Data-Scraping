# I, Saras - Data Scientist Assignment



## Task 1

Modules needed
1. ***[PyPDF2](https://pypi.org/project/PyPDF2/)*** to read and handle the pdf files
2. ***CSV*** (Built-in) to read and write data in a CSV format

#### The pdf to be parsed is located in the same folder as the main.py , which is read and broken down into separate article at first, followed by segmenting them into Number, title and body based of the format of the strings. 
Then the segments are stored in a Dictionary variable which is fed into the CSV file.


## Task 2

Modules used
1. ***[BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)*** to scrape and manipulate the data from the given URL 
2. ***Requests***  to send HTTPS requests and fetch the responses
3. ***SQLite3*** to manage the database which store the scraped data provided by the BeautifulSoup functions

#### All the business article URLs are extracted from the initial site, which are then individually broken down to get the necessary data which are then pushed into a news.db database file with SQLite3 functionalities.

