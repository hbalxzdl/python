import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36 OPR/63.0.3368.53'
    }
    data = requests.get(url, headers=headers, verify=False).content

    return data


def get_li(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    ul = soup.find('div', attrs={'class': 'nl_con'})

    house = []

    for item in ul.find_all('div', attrs={'class': 'nlc_details'}):
        # 小区名称
        li = item.find('div', attrs={'class': 'nlcd_name'})
        nlcd_name = li.find('a').get_text().strip()

        print(nlcd_name)
        # 区域
        sngrey = item.find('span', attrs={'class': 'sngrey'})
        if sngrey is None:
            area =''
        else:
           area = sngrey.get_text().strip()
 
        # 地址
        address = item.find('div', attrs={'class': 'address'}).a['title']

        house.append([nlcd_name, area, address])

    # 获取下一页
    page = soup.find('div', attrs={'class': 'page'}).find(
        'a', attrs={'class': 'active'}).next_sibling.next_sibling

    if page:
        return house, page['href']
    return house


def main():
    url = 'https://cs.newhouse.fang.com/house/s/b99'
    page = 1
    info_result = []
    while page <5:
        doc = download_page(url)
        info_list, next_url = get_li(doc)
        url += next_url
        page += 1
        info_result += info_list

    wb = Workbook()
    ws = wb.active
    for row in info_result:
        ws.append(row)
        wb.save("e:\\sample.xlsx")


if __name__ == '__main__':
    main()
