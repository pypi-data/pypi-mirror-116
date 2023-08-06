
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup

class Init:
        async def init(self,link):
         self.link2=link
        
         session = AsyncHTMLSession()
         response = await session.get(self.link2)
         await response.html.arender(sleep=1,timeout=30)
         return BeautifulSoup(response.html.html, "html.parser") 
     