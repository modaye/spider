# _*_coding: utf-8 _*_
# @Time: 2021/6/28 0028 22:53
# @Author: >瓦瓦<
# @QQ: 3252219120
# @File: main.py
"""
笔趣阁小说网爬虫
指定一本小说
requests
bs4
"""
from typing import Optional, Dict, List, Tuple
import requests
from bs4 import BeautifulSoup


def request_url(url: str, headers: Dict[str, str] = None, params: Dict[str, str] = None) -> requests.Response:
    """
    get 请求 下载网页
    :param url: 统一资源定位符 （网址）
    :param headers: 请求头 一般带上user-agent
    :param params: 请求参数  requests 自动拼接字典形式的参数
    :return: Response 对象
    """
    res = requests.get(url, headers=headers, params=params)

    # 如果不返回200 ok引发异常
    res.raise_for_status()

    # 编码
    res.encoding = 'gbk'
    return res


def parse_chapter(res: requests.Response) -> List[Tuple[str, str]]:
    """
    解析章节列表
    :param res: 返回对象
    :return:
    """
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')  # lxml解析更快
    urls = []
    for dd in soup.find(name='div', class_='listmain').dl.find_all(name='dd'):
        url = dd.a['href']
        title = dd.a.get_text(strip=True)
        urls.append((title, url))
    return urls


def parser_content(res: requests.Response):
    """
    :param res:
    :return:
    """
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    # 列表解析式
    contents = [br.get_text(strip=True) for br in soup.find("div", id='content').find_all('br')]
    content = '\n'.join(contents)
    return content


def main(start_url, base):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 Safari/537.36 '
    }
    res = request_url(url=start_url, headers=headers)
    for title, url in parse_chapter(res):
        url = base + url
        res = request_url(url=url, headers=headers)
        content = parser_content(res)
        print(f"{title}:{url} 爬取完成...")


if __name__ == '__main__':
    # 沧元图
    url = "https://www.bqkan8.com/38_38836/"
    base_url = "https://www.bqkan8.com"  # 域名
    main(start_url=url, base=base_url)