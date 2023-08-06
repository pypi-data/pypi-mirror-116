  
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

from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession

import urllib.request
import time

import re
from pytube import YouTube
import asyncio
from functools import wraps
from . import Init
class crawl(Init):
    def __init__(self,video_name:str="",video_id:str="",output: str = "",video_link:str=''):
        if " " in video_name:
            video_name=video_name.split()
            video_name="+".join(video_name)
        self.name = video_name
        
        self.id = video_id
        self.out= output
        self.link = video_link
        if not self.name:
            if not self.id:
              if not self.link:
                raise ValueError("Provide Video Name Or Video Link or video id, Please.")
        if self.link:
            self.link=self.link
        elif self.id:
            self.link="https://www.youtube.com/watch?v=" + self.id
        elif self.name:        
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+ self.name)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            self.vidid=video_ids[0]
            self.link="https://www.youtube.com/watch?v=" + self.vidid
    
        self.link2=self.link
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent':user_agent} 
        self.link=self.link2
    async def knit(self):
        await self.init(self.link)

    async def keyword(self):
        await self.init(self.link)     
        self.title = self.soup.find("meta",attrs={"name":"keywords"})
        
        return self.title["content"]
        
    async def videolink(self):
        return self.vidid
    
    async def VideoDetails(self):

        likes=(await self.likes_dislikes)()[1]
        dislikes=(await self.likes_dislikes)()[2]
        if dislikes == "Dislike":
            dislikes= "N/A"
        title=(await self.upload_time_and_title())[0]
        upload=(await self.upload_time_and_title())[1]
        params = {
         "Video Title": title,
         "Video Id" :(await self.videolink()).split("/")[-1], 
         "Description": await self.description(),
         "Veiws": await self.veiws(),
         "Likes": likes,
         "Dislikes": dislikes,
         "Upload Time": upload,
         "Video Link":await self.videolink(),
         "Channel" : await self.channel()
        }
        return params
        
    async def likes_dislikes(self):
        await self.init(self.link)
        likes_dislikes=[]
        for i in self.soup.find_all("yt-formatted-string",{"id":"text"}):
            likes_dislikes.append(i.get_text())
        return likes_dislikes
    
    async def upload_time_and_title(self):
        det=[]
        await self.init(self.link)
        title=self.soup.find_all("yt-formatted-string",{"class":"style-scope ytd-video-primary-info-renderer"})
        for i in title:
            det.append(i.get_text())
        print(det)
        return det

    async def VidTitle(self):
        return (await self.upload_time_and_title())[0]

    async def videoUploadTime(self):
        return (await self.upload_time_and_title())[1]
        

    async def description(self):
        descrip=''
        await self.init(self.link)
        for i in self.soup.find_all("span",{"class":"style-scope yt-formatted-string"}):
            descrip+=i.get_text()
        return descrip
    
    async def channel(self):
        channelinfo={}
        await self.init(self.link)
        name=self.soup.find("yt-formatted-string", {"class": "ytd-channel-name"})
        tg=name
        name=name.find("a").text
        channelink=self.soup.find("a",{"class":"yt-simple-endpoint style-scope ytd-video-owner-renderer"})
        channelink=channelink.get("href")
        subs=self.soup.find("yt-formatted-string",{"id":"owner-sub-count"})
        subs=subs.get_text()
        channelinfo.update({"name":name,"channel_link":"https://www.youtube.com"+ channelink,
        "subscriber": subs                
        })
        return channelinfo
    
    async def download(self,to_mp3:bool=False,mp3name:str=''):
        
        if not self.out:
            path='.'
        else:
            path=self.out
        yt = YouTube(self.link2)
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        yt.download(path)
                
    async def veiws(self):
        await self.init(self.link)
        veiws=self.soup.find("span",{"class":"view-count style-scope ytd-video-view-count-renderer"})
        return veiws.text
    
    async def videolink(self):
      await self.init(self.link)
      ida=self.soup.find("link",{"rel":"shortlinkUrl"})
      return ida.get("href")

