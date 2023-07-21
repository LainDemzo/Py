# 5000a28fd8e0156a661744681a080b77
# https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={openweatherAPI}&units=metric

import asyncio
import os
import re
import aiohttp

wea_api = 'c4899e8156ba90ed45c422556eefd751'
wea_url = 'https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={wea_api}&units=metric'
city = 'city/cities.txt'


class Wheather:

    def __init__(self, file_citys, wea_api):
        self.file_citys = file_citys
        self.wea_api = wea_api
        self.list_citys = []
        self.import_file_citys()
        self.weather = {}

    def import_file_citys(self):
        file = open(os.path.join(self.file_citys), 'r')
        for i in file:
            se = re.findall('\d+\)(?:\s)?(.+?)(?:\s)?-', i)
            if se:
                self.list_citys.append(se[0])

    async def getrequest(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                req = await response.text()
                if req:
                    return req
                else:
                    return False

    async def getweather(self):
        date = []
        tasks = []
        for i in self.list_citys:
            task = asyncio.create_task(self.getrequest(
                f'https://api.openweathermap.org/data/2.5/weather?q={i}&appid={self.wea_api}&units=metric'))
            tasks.append(task)
        data = await asyncio.gather(*tasks)

        if data:
            # print(data)
            for i in data:
                name = re.findall(r'\"name\":\"(.+?)\"', i)[0]
                temp = re.findall(r'\"temp\":(.+?),', i)[0]
                pressure = re.findall(r'\"pressure\":(.+?),', i)[0]
                self.weather[name] = {"city": name, "temp": temp, "pressure": pressure}
            return self.weather
        else:
            return False

    def start(self):
        asyncio.run(self.getweather())


wea = Wheather(file_citys=city, wea_api=wea_api)
wea.start()
print(wea.weather)
