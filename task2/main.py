import requests
from bs4 import BeautifulSoup
import re
import sqlite3 



def main():
    try:
        links= extractlinks("https://www.indianexpress.com") #extract all business links in the page
        feedToDB(links) #feeding the link contents to database
    except:
        print("Invalid URL")
    
 

##------Function to extract article links-------##
def extractlinks(url):
    links=[]
    try:
        r=requests.get(url)
        soup= BeautifulSoup(r.content, 'html.parser')
        linlist= soup.find_all('a', attrs={"href":re.compile("/article/business/")})
        
        for lin in linlist:
            links.append(lin.get('href'))
    except:
        print("Unable to extract articles")

    #convert it into a set and back to eliminate duplicate links
    return list(set(links))  


##--------Function to mine information from each article link -----------##
def getInfo(url):
    
    try:
        r=requests.get(url)
        soup= BeautifulSoup(r.content, 'html.parser')

        # ! We are encoding all text content into ascii and ignoring illegal characters for simplicity
        title= str(soup.find('meta', attrs={"itemprop":"headline"}).get("content").encode("ascii","ignore"))

        if soup.find('meta', attrs={"itemprop":"author"}):
            author= soup.find('meta', attrs={"itemprop":"author"}).get("content")
        else :
            author= "Null" #if author name is missing in the article

        pub_date= soup.find("meta",attrs={"itemprop":"datePublished"}).get("content")
        
        body=""
        paras=soup.findAll('p', attrs={"class":None})
        for para in paras:
            body+=str(para.get_text().encode('ascii','ignore')).replace("\\n","")
        
        return {'title':title, 'author':author, 'pub':pub_date, 'body':body}

    except:
        return {'Message':"Issue with parsing"}


##---feeding the info given from each article into Table ---## 

def feedToDB(links):
    try:
        conn = sqlite3.connect('./task2/news.db')
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS Business
                    (id INTEGER PRIMARY KEY, title TEXT UNIQUE, author, publication_date,body )''')
        cursor.execute('SELECT COUNT(ID) FROM Business')
        key=int(cursor.fetchone()[0])   #to continue the IDs after the pre-existing entries/rows' 

        for link in links:
            temp=getInfo(link)
            #error handling for duplicate entries.
            try:
                cursor.execute(f'''INSERT INTO Business VALUES {key,temp['title'],temp['author'],temp['pub'][0:10],temp['body']}''')
            except:
                key=key-1

            key=key+1

        #---use this to view the table in text--#
        # cursor.execute("SELECT * FROM Business")
        # file2=open("./task2/table.txt",'w')
        # file2.write(str(cursor.fetchall()))
        # file2.close()

        conn.commit()
        conn.close()  
    except:
        print("Trouble accessing Database")


if __name__ == "__main__":
    main()
