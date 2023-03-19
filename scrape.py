# Web Scraper Using HTML
from bs4 import BeautifulSoup as bs
import requests
import lxml
import logging
from multipledispatch import dispatch


class Scrape:

    # Created the session and soup
    session = requests.session()
    soup = bs()

    # URL and Browser Data
    URL = 'https://alumnifinderonline.com/'
    LOGIN = 'Login'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'origin': URL,
        'referer': URL + LOGIN
    }

    #Logging Info
    logging.basicConfig(level=logging.INFO)

    
    def __init__(self, username:str, password:str):
        self.login(username, password)

    def login(self, username:str, password:str):
        payload = {
            'UserName': f'{username}',
            'Password': f'{password}',
            'RememberMe': 'false'
        }
        self.session.post(self.URL + self.LOGIN, headers = self.HEADERS, data = payload)
        logging.info("Logged In AlunmiFinder")
    
    

    @dispatch(object) 
    def scrapePersonInfo(self, info:dict):
        multSoup:bs=[]
        #Search person

        info = self.session.post(self.URL + 'Search/PersonSearch_Basic', headers = self.HEADERS, data = info)
        self.soup = bs(info.text, 'lxml')
        if self.errorHandler(self.soup): return None
        multSoup.append(self.soup)

        
        while True:
            nextPageLink = self.getNextPage(self.soup)
            if not nextPageLink:
                return multSoup
            self.soup = bs(self.session.get(nextPageLink).text, 'lxml')
            multSoup.append(self.soup)


        

    @dispatch(str) 
    def scrapePersonInfo(self, lex_id: str):
        multSoup:bs = []
        payload = {
            'LexId': f'{lex_id}'
        }
        info = self.session.post(self.URL + 'Search/PersonSearch_Basic', headers = self.HEADERS, data = payload)
        self.soup = bs(info.text, 'lxml')
        if self.errorHandler(self.soup): return None

        multSoup.append(self.soup)

        while True:
            nextPageLink = self.getNextPage(self.soup)
            if not nextPageLink:
                return multSoup
            self.soup = bs(self.session.get(nextPageLink).text, 'lxml')
            multSoup.append(self.soup)

    
    def errorHandler(self, soup):
        if soup.find('div', {'class': "form-group text-danger"}).find('span') is not None:
            logging.error('Error:', soup.find('div', {'class': "form-group text-danger"}).find('span').text.strip())
            return True
        return False

    def getNextPage(self, soup):
        if len(soup.find_all('li', {'class': 'PagedList-skipToNext'})) == 0:
            return
        page = soup.find('ul', {'class': 'pagination pagination-sm'})
        next_page = self.URL + str(page.find('li', {'class': 'PagedList-skipToNext'}).find('a')['href'])
        return next_page




    
