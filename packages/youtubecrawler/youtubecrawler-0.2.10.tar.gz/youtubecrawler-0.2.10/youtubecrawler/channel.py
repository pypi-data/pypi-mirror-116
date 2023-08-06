 
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

import re
from requests.sessions import session
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
from collections import OrderedDict



from  .crawl import crawl
class channel:
    def __init__(self,channel_id:str='',channellink:str="",channelname:str=''):
        self.session = HTMLSession()
        if channel_id:
            self.channel="https://www.youtube.com/channel/" + channel_id
        elif channellink:
            self.channel=channellink
        elif channelname:
            if " " in channelname:
                channelname=channelname.split()
                channelname="+".join(channelname)
            response = self.session.get("https://www.youtube.com/results?search_query=" + channelname)
            response.html.render(sleep=1,keep_page=True,timeout=30)
            
            soup = BeautifulSoup(response.html.html, "html.parser") 
            self.channel=soup.find("a",{"class":"channel-link yt-simple-endpoint style-scope ytd-channel-renderer"}).get("href")
            self.id=self.channel
            self.channel="https://www.youtube.com" + self.channel
        else:
            raise ValueError("No Paramter is provided")
        response = self.session.get(self.channel)
        response.html.render(sleep=1,keep_page=True,timeout=30)
        self.soup = BeautifulSoup(response.html.html, "html.parser") 
        
        response.session.close()
    def subs(self):
            return self.soup.find("yt-formatted-string",{"id":"subscriber-count"}).text
     
    
    def about(self):
        response = self.session.get('https://www.youtube.com' + self.id + "/" + "about")
        response.html.render(sleep=1,keep_page=True,timeout=30)
        soup = BeautifulSoup(response.html.html, "html.parser")  
        response.session.close()
        return soup

    def description(self):
        self.chan=self.about()
        return self.chan.find("yt-formatted-string",{"id":"description"}).text 
    
    
    def joined(self):
        about=self.about()
        j=[]
        for i in about.find_all("span",{"class":"style-scope yt-formatted-string"}):
        
            j.append(i.get_text())
        jp=int(j.index("Joined "))
        return j[jp +1]
    
    
    def links(self):
        print("Getting Links of about Please wait!!!")
        print("Processing Request")
        lip=self.about()
        li={}
        laps=[]
        gaps=[]
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':user_agent} 
        for p in lip.find_all("yt-formatted-string",{"class":"info-text style-scope ytd-channel-about-metadata-renderer"}):
            for x in lip.find_all("a",{"class":"yt-simple-endpoint style-scope ytd-channel-about-metadata-renderer"}):
                x=x.get('href')
                if x.find("redirect") != -1:
                 
                 session=HTMLSession()
                 response = session.get(x)
                 response.html.render(sleep=1,keep_page=True,timeout=30)
                 x = BeautifulSoup(response.html.html, "html.parser")  
                 response.session.close()
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

    def latest_video(self):
     print('https://www.youtube.com' + self.id + "/" + "videos")
     response = self.session.get('https://www.youtube.com' + self.id + "/" + "videos")
     response.html.render(sleep=1,keep_page=True,timeout=30)
     soup = BeautifulSoup(response.html.html, "html.parser")  
     op=soup.find("a",{"id":"thumbnail"}).get('href')
     response.session.close()
     op=crawl(video_link="https://www.youtube.com" + op)
     return {"Latest Video" : op.VideoDetails()}
    
    def latest_community(self):
     response = self.session.get('https://www.youtube.com' + self.id + "/" + "community")
     response.html.render(sleep=1,keep_page=True,timeout=30)
     soup = BeautifulSoup(response.html.html, "html.parser")  
     comun=soup.find("yt-formatted-string",{"id":"content-text"}).text
     response.session.close()
     return comun
 
    def spareChannels(self):
      session=HTMLSession()
      response = session.get('https://www.youtube.com' + self.id + "/" + "channels")
      response.html.render(sleep=1,keep_page=True,timeout=30)
    
      soup = BeautifulSoup(response.html.html, "html.parser")
      response.session.close()
      channels={}
      for i in soup.find_all("div",{"id":"channel"}):
           response = session.get('https://www.youtube.com' + i.find("a")['href'])
           response.html.render(sleep=1,keep_page=True,timeout=30)
           soup = BeautifulSoup(response.html.html, "html.parser")
           channels.update({i.find('span').text:{"Link":'https://www.youtube.com' + i.find("a")['href'],"Subscribers":soup.find("yt-formatted-string",{"id":"subscriber-count"}).text }})
      response.session.close()
      return channels
