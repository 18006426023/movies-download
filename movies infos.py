import requests
from lxml import etree
import lxml
import csv

BASE_DOMAIN = 'https://www.dytt8.net'
HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}


def get_detail_urls(url):
        response = requests.get(url, headers=HEADERS)
        text = response.text
        text = text.replace('0xfc', ' ').replace('0xd0', ' ')
        html = etree.HTML(text)
        urls = html.xpath("//table[@class='tbspan']//a//@href")
        url_list = []
        for url in urls:
                url = BASE_DOMAIN + url
                url_list.append(url)
        return(url_list)


def parse_page(url):
        response = requests.get(url, headers=HEADERS)
        text = response.content.decode('gbk')
        text = text.replace('0xfc', ' ').replace('0xd0', ' ')
        html = etree.HTML(text)
        # title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
        # img = html.xpath("//*[@id='Zoom']//img/@src")[0]
        infos = html.xpath("//*[@id='Zoom']//text()")
        movies = {'片名': '0', '年代': '0', '产地': '0', '类别': '0', '评分': '0', '下载链接': '0'}
        for info in infos:
                if info.startswith('◎年　　代'):
                        year = info.replace('◎年　　代', '').strip()
                        movies['年代'] = year
                elif info.startswith('◎豆瓣评分'):
                        score = info.replace('◎豆瓣评分', '').strip()
                        if score[0:3] == '/10':
                                score = '0'
                        movies['评分'] = score[0:3]
                elif info.startswith('◎产　　地'):
                        place = info.replace('◎产　　地', '').strip()
                        movies['产地'] = place
                elif info.startswith('◎译　　名'):
                        title = info.replace('◎译　　名', '').strip().split('/')
                        movies['片名'] = title[0]
                elif info.startswith('◎类　　别'):
                        title = info.replace('◎类　　别', '').strip()
                        movies['类别'] = title
        if html.xpath("//td[@bgcolor='#fdfddf']//a/text()"):
                download_url = html.xpath("//td[@bgcolor='#fdfddf']//a/text()")[0]
                movies['下载链接'] = download_url
        return movies



if __name__ == '__main__':
        urls = ['https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'.format(str(i)) for i in range(0, 195)]
        csvfile = open("movies.csv", 'w+', newline='')
        try:
                writer = csv.writer(csvfile)
                writer.writerow(('片名', '年代', '产地', '类别', '豆瓣评分', '迅雷下载链接'))
                for url in urls:
                        detail_urls = get_detail_urls(url)
                        for url in detail_urls:
                                movies = parse_page(url)
                                print(movies)
                                writer.writerow((value for value in movies.values()))
        finally:
                csvfile.close()





