  
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

from . import Init

import re
from requests.sessions import session
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
from collections import OrderedDict

from .asynced import crawl as Crawl
class channel(Init):
    def __init__(self,**args):
      channel_id=args.get("channel_id")
      channellink=args.get('channel_link')
      channelname=args.get("channelname")
      if " " in channelname:
           channelname=channelname.split()
           channelname="+".join(channelname)
      self.channel_id=channel_id
      self.channellink=channellink
      self.channelname=channelname
    async def Ainit(self): 
      
        if self.channel_id:
            self.channel="https://www.youtube.com/channel/" + self.channel_id
            self.chanid=self.channel_id
        elif self.channellink:
       
            self.channel=self.channellink
            c=Crawl(video_link=self.channel)
            self.chanid=(await c.videolink()).split("/")[-1]
        elif self.channelname:
            soup =await  self.init("https://www.youtube.com/results?search_query=" + self.channelname)
            self.channel=soup.find("a",{"class":"channel-link yt-simple-endpoint style-scope ytd-channel-renderer"}).get("href")
            self.chanid=self.channel
            
            self.channel="https://www.youtube.com" + self.channel
        else:
            raise ValueError("No Paramter is provided")
        self.chanid=self.chanid
        
    async def subs(self):
            await self.Ainit()
            self.soup=await self.init(self.channel)
            return self.soup.find("yt-formatted-string",{"id":"subscriber-count"}).text
     
    
    async def about(self):
       await self.Ainit()

       return await self.init('https://www.youtube.com' + self.chanid + "/" + "about")

    async def description(self):
        await self.Ainit()
        self.chan= await self.about()
        return self.chan.find("yt-formatted-string",{"id":"description"}).text 
    
    
    async def joined(self):
        await self.Ainit()
        about=await self.about()
        j=[]
        for i in about.find_all("span",{"class":"style-scope yt-formatted-string"}):
        
            j.append(i.get_text())
        jp=int(j.index("Joined "))
        return j[jp +1]
    
    
    async def links(self):
        await self.Ainit()
        print("Getting Links of about Please wait!!!")
        print("Processing Request")
        lip=await self.about()
        li={}
        laps=[]
        gaps=[]
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':user_agent} 
        for p in lip.find_all("yt-formatted-string",{"class":"info-text style-scope ytd-channel-about-metadata-renderer"}):
            for x in lip.find_all("a",{"class":"yt-simple-endpoint style-scope ytd-channel-about-metadata-renderer"}):
                x=x.get('href')
                if x.find("redirect") != -1:
                 
                 x = self.init(x)
                 x=x.find_all("div",attrs={"id":"redirect-action-container"})
                 for i in x:
                     x=i.find("a")['href']
                laps.append(x)
                    
                gaps.append(p.text)
        gaps=list(OrderedDict.fromkeys(gaps))
        laps=list(OrderedDict.fromkeys(laps))
        for i,p in zip(gaps,laps):
            li.update({i:p})
        
        return li

    async def latest_video(self):
     await self.Ainit()
     soup =await self.init('https://www.youtube.com' + self.chanid + "/" + "videos")
     op=soup.find("a",{"id":"thumbnail"}).get('href')
     op=Crawl(video_link="https://www.youtube.com" + op)
     return {"Latest Video" : await op.VideoDetails()}
    
    async def latest_community(self):
     await self.Ainit()
     soup = await self.init('https://www.youtube.com' + self.chanid + "/" + "community")
     comun=soup.find("yt-formatted-string",{"id":"content-text"}).text
     return comun
 
    async def spareChannels(self):
      await self.Ainit()
      soup=await self.init(self.channel)

      channels={}
      for i in soup.find_all("div",{"id":"channel"}):
           soup = await self.init('https://www.youtube.com' + i.find("a")['href'])
           channels.update({i.find('span').text:{"Link":'https://www.youtube.com' + i.find("a")['href'],"Subscribers":soup.find("yt-formatted-string",{"id":"subscriber-count"}).text }})
      return channels
