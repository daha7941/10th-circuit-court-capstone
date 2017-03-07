import re
import requests
import time
from pymongo import MongoClient
from bs4 import BeautifulSoup

def init_mongodb():
    #Mongo database and table
    db_client = MongoClient()
    db = db_client['case_database']
    coll = db.cases
    return db.cases

def case_scrape(cfile):
    '''
    need multiple queries, one for the actual text, one for cases ref(note: not all cases have the related case tag, might need to implement some RE to grap the rest), grab case title?
    '''
    r = requests.get(cfile)
    web_data=r.text
    soup = BeautifulSoup(web_data,'html.parser')
    '''
    from http://law.justia.com/cases/federal/appellate-courts/ca10/2000/ grabs all links of listed 2000 court cases
    note: started with 2017 cases but most were listed as pdf files while the 2000 cases were in a text format
    '''
    link_list=[]
    mylinks=soup.findAll('a',{'class':'case-name'})
    for l in mylinks:
        link_list.append(l['href'])
    return link_list

def link_scape(list_of_links, table):
    '''
    links in list_of_links only contain the second half of neede link, need to add base link to query them
    '''
    base_link='http://law.justia.com/'

    for i,v in enumerate(list_of_links):
        list_of_links[i]=base_link+v

    for lnk in list_of_links:
        link_r = requests.get(lnk)
        new_data=link_r.text
        link_soup = BeautifulSoup(new_data,'html.parser')
        #grabs full case text
        link_text=''
        for page in link_soup.findAll('div',{'class':'page'}):
            link_text+=page.get_text()
        title_text=''
        for x in link_soup.findAll('h1',{'class':'heading-1'}):
            title_text+=x.get_text()
        #makes list of case_ref
        #re expression to pull case refs
        re_list = re.findall('(\d+\s\D\.\D*\w+\s\d*)',link_text)
        add_new = [{'case_title':title_text,'case_text':link_text, 'case_ref':re_list}]
        table.insert(add_new)
        time.sleep(9)

        # outdated code, not all case refs had a class
        # case_ref=[]
        # mya = soup.findAll('a',{'class':'related-case'})
        # for a in mya:
        #     case_ref.append(a.text.strip())
if __name__ == '__main__':
    #start db
    cases = init_mongodb()
    #get links to scrape
    linklist = case_scrape('http://law.justia.com/cases/federal/appellate-courts/ca10/2000/')
    #scrape and add data
    link_scape(linklist,cases)
