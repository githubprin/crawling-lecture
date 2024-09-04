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
    print(url)
    response = await session.get(url)
    
    if response.status == 200:
        print("good")
        
        text = await response.text()
        
        soup = BeautifulSoup(text, 'html.parser')
            
        press_lists = soup.find_all('li', {'class': 'journalist_list_content_item'})
        
        press_info = []
        for press_list in press_lists:
            a = press_list.find('a', {'class': 'journalist_list_content_name'})
            name = a.text
            link = a['href']
            journalist_tuple = (name, link)
            press_info.append(journalist_tuple)
            
        code2name[press_code] = (code2name[press_code], press_info)
    
    await response.release()
    
async def acrawl_journalist_info_pages(code2name):
    session = aiohttp.ClientSession()
    
    tasks = [afetch_journalist_list(press_code, session) for press_code in code2name]
    
    results = await asyncio.gather(*tasks)
        
    await session.close()
    
if __name__ == '__main__':
    code2name = crawl_press_names_and_codes()
    begin = time()
    asyncio.run(acrawl_journalist_info_pages(code2name))
    end = time()
    print(end - begin)