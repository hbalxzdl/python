import requests
from bs4 import BeautifulSoup


class Aikecheng(object):
    def __init__(self, url):
        self.url = url

    def page(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36 OPR/63.0.3368.53'
        }
        data = requests.get(self.url, headers=headers, verify=False).content
        return data

    def dataList(self, doc):
        soup = BeautifulSoup(doc, 'html.parser')
        ul = soup.find('section', attrs={'class': 'icourse-open-panel'}).find('ul',
                                                                              attrs={'class': 'icourse-open-list'})
        lis = ul.find_all('div', attrs={'class': 'icourse-item-modulebox-mooc'})

        listData = []
        for item in lis:
            desc = item.find('div', attrs={'class': 'icourse-desc'})
            # 课程名称
            descName=desc.find('p', attrs={'class': 'icourse-desc-top-mooc'}).find_all('b')

            # 开课时间
            descTime = desc.find('p', attrs={'class': 'icourse-desc-bottom-mooc'}).span.get_text().strip()

            #网址链接
            descLink=desc.find('p', attrs={'class': 'icourse-desc-top-mooc'}).a['href']

            descStr = ''

            for value in descName:
                descStr += value.get_text().strip()

            listData.append({'name': descStr,'time':descTime,'link':descLink})


        print(listData)

url = 'http://www.icourses.cn/oc/'
kecheng = Aikecheng(url)

kecheng.dataList(kecheng.page())
