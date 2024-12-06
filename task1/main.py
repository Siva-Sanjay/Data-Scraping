import PyPDF2  as p
import re
import csv


def main():
    try:
        a =  p.PdfReader("./task1/sample.pdf")
        
        articles=listifyArticles(a.pages)
        
        #parsing articles into needed segments 
        parsed_articles=[]
        i=1
        while i<len(articles):
            parsed_articles.append({
                "s_no":articles[i][0:articles[i].index(". ")].strip(),
                "article_title":articles[i][articles[i].index(". ")+2:-3].strip(),
                "article_body":articles[i+1].strip().replace("\\n","")
            })
            i=i+2

        feedCSV(parsed_articles)
    except:
        print("Unable to read PDF, check the file and location")
        

## ---- Feeding the data into CSV ------##
def feedCSV(parsed_articles):
    try:
        with open("./task1/output.csv",mode="w",newline="",encoding="ascii") as file:
            write=csv.DictWriter(file,fieldnames=["s_no","article_title","article_body"])
            write.writeheader()
            for row in parsed_articles:
                write.writerow(row)
        print("Successfully written in CSV")
    except:
        print("Error while writing in CSV")



##----- Breakdown the pdf into articles and making a list ---##
def listifyArticles(pages):
    text=""
    #all pages exluding the last unnecessary pages
    #ignore non ascii characters for readability and removing watermark texts
    #Only pages of considerable lenght (>30) and not index pages
    try:
        for page in pages[0:-8]:
            temp= str(page.extract_text().encode("ascii", "ignore")).replace("Vision IAS","").replace("www.visionias.in","")
            
            if len(temp)>30 and isNotIndex(temp):
                text+= temp 

        # split by article 
        # for simplicity articles with indices like 1.1, 2.3 are considered. 
        # Whole number indices are ignored and 
        # other sub articles include under their respective articles 

        text = re.sub(r'\s{2}\d+\.\s[A-Z\s]+\\n','',text)  #elimiating bigger headings
        articles= re.split(r'[\s\\n](\d+\.\d+\.\s[A-Z]+[^a-b]*?\\n)',text) 
    except:
        print("Error occured at splitting articles, check your pdf file")

    return articles


##---- ensuring if a page isnt index page ---##
def isNotIndex(text):
    #number of dashed lines terminating with numbers are counted
    lines = re.split(r'\\n', text.strip())
    count=0
    for line in lines:
        if re.match(r'._*.+\d+$', line.strip()):
            count+=1
    #if dashed lines consititue a significant portion of the full page
    if count > len(lines)* 0.5:
        return False
    else :
        return True



if __name__ == "__main__":
    main()
