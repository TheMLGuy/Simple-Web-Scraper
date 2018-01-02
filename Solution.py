from bs4 import BeautifulSoup
import requests
import math
import time


start_url='https://www.macys.com'
domain='https://www.macys.com'

''' get soup '''
def get_soup(url):
    # get contents from url
    content=''
    while content=='':
        try:
            content = requests.get(url,
                               headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}).content
        except:
            time.sleep(5)
            continue
    return BeautifulSoup(content,'lxml') # choose lxml parser

'''find all anchor tags'''
def findAllATags(url):
    soup = get_soup(url)
    a_tags = soup.findAll('a')
    a_tags=[a for a in [a for a in a_tags if 'href' in a.attrs] if a.attrs['href'].find('/shop')==0]
    return a_tags

'''print all 'title' attributes'''
def printTitles(url,f):
    soup=get_soup(domain+url)
    temp=[i.find('a') for i in soup.findAll('div',{'class':'productThumbnailImage'})]
    for i in temp:
        f.write(i['title']+'\n')
    
'''iterate through all pages for each soup object'''
def pagination(count, url,f,u):
    count_=math.ceil(count/60)
    i=2
    printTitles(url,f)
    u.write(url+'\n')
    while i<=count_:
        printTitles(url.replace("?","/Pageindex/"+str(i)+"?"),f)
        i+=1
'''filehandlers for output.txt and urlHandler.txt'''
def fileHandler():
    f=open('output.txt','a')
    return f
def urlHandler():
    f=open('urlHandler.txt','a')
    return f
'''generates soup object for each url'''
def getItems(url):
    soup=get_soup(domain+url)
    try:
        f=fileHandler()
        u=urlHandler()
        f.write(soup.find('span', {'id' : 'currentCategory'}).text+'\n')
        pagination(int(soup.find('span',{'id':'productCount'}).text),url,f, u)
    except:
        pass
    finally:
        f.close()
        u.close()

'''main function'''
if __name__=='__main__':
    start_time=time.time()
    items=[]
    tags=findAllATags(url=start_url)
    '''executing getItems for tags[12:] because first 11 have no relevant information'''
    for i in tags[12:]:
        getItems(i.attrs['href'])
    print(time.time()-start_time)
