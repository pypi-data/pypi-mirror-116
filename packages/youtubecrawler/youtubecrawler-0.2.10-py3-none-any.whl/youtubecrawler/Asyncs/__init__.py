
from re import L
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import requests
from threading import Thread
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession


class Init:
        async def init(self,link):
         self.link2=link
        
        
         session = AsyncHTMLSession()
         response = await session.get(self.link2)
         await response.html.arender(sleep=1,keep_page=True,timeout=30)
       

          
          
         self.soup = BeautifulSoup(response.html.html, "html.parser") 
         await response.session.close()
         