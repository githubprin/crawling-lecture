import asyncio
import aiohttp

import requests
from bs4 import BeautifulSoup
from time import time

def crawl_press_names_and_codes():
    """Make the dict that have press code as key, and press name as value. Crawl from https://media.naver.com/channel/settings. 
    """
    url = 'https://media.naver.com/channel/settings'
    code2name = {}
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        new_list = soup.find_all('li', {'class': 'ca_item _channel_item'})
        
        for news in new_list:
            press_code = news['data-office']   
            press_name = news.find('div', {'class': 'ca_name'}).text
            code2name[press_code] = press_name
    
    return code2name 

async def afetch_journalist_list(press_code, session):
    url = f'https://media.naver.com/journalists/whole?officeId={press_code}'
    # print(url)
    # await asyncio.sleep(1)
    
    async with session.get(url) as response:
        if response.status == 200:
            soup = BeautifulSoup((await response.text()), 'html.parser')
            
            press_lists = soup.find_all('li', {'class': 'journalist_list_content_item'})
            
            press_info = []
            
            for press_list in press_lists:
                a = press_list.find('a', {'class': 'journalist_list_content_name'})
                name = a.text
                link = a['href']
                journalist_tuple = (name, link)
                press_info.append(journalist_tuple)
        
            return press_info

async def acrawl_journalist_info_pages(code2name):
    """Accepts press code - press name dict, and return dict having press code as key, and 2-tuple of (press name, listof 2-tuple containing journalist name and their link) as value. 

    For now, you DO NOT have to crawl all journalists; for now, it's impossible. 
    Crawl from https://media.naver.com/journalists/. 
    """
    # async with aiohttp.ClientSession() as session:
    session = aiohttp.ClientSession()
    
    tasks = [afetch_journalist_list(press_code, session) for press_code in code2name]
    # for press_code in code2name:
    #     await afetch_journalist_list(press_code, session)
    
    results = await asyncio.gather(*tasks)
    
    await session.close()
    print(results)
    
    # from code import interact
    # interact(local = locals())
    
    # ######################## 돌아오는 result 활용 부분
    
    code2name[press_code] = (code2name[press_code], press_info)
        
    # return code2name 

class Journalist:
    def __init__(self, name, press_code, 
                career_list, 
                graduated_from, 
                no_of_subscribers, 
                subscriber_age_statistics, 
                subscriber_gender_statistics, 
                article_list):
        self.name = name 
        self.press_code = press_code 
        self.career_list = career_list
        self.graduated_from = graduated_from
        self.no_of_subscribers = no_of_subscribers
        self.subscriber_age_statistics = subscriber_age_statistics
        self.subscriber_gender_statistics = subscriber_gender_statistics
        self.article_list = article_list 


def crawl_journalist_info(link):
    """Make a Journalist class instance using the information in the given link. 
    """
    
            
if __name__ == '__main__' : 
    code2name = crawl_press_names_and_codes()
    begin = time()
    asyncio.run(acrawl_journalist_info_pages(code2name))
    end = time()
    print(end - begin)