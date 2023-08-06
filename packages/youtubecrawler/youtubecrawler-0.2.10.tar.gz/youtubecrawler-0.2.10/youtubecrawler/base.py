  
#    Copyright 2021 KeinShin
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#        http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
class Init:
        async def init(self,link):
         self.link2=link
        
         session = AsyncHTMLSession()
         response = await session.get(self.link2)
         await response.html.arender(sleep=1,timeout=30)
         return BeautifulSoup(response.html.html, "html.parser") 
    