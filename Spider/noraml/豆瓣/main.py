# _*_coding: utf-8 _*_
# @Time: 2021/6/29 0029 22:11
# @Author: >瓦瓦<
# @QQ: 3252219120
import time
from typing import Dict

import requests
from bs4 import BeautifulSoup
import lxml


def request_url(url: str, headers: Dict[str, str], params: Dict[str, str] = None) -> requests.Response:
    """
    下载网页
    :param url: 网址
    :param headers: 请求头
    :param params: 参数
    :return: response
    """
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()

    # 自动判断encoding
    res.encoding = res.apparent_encoding

    return res


def parse_link(res: requests.Response):
    """
    解析链接 标题, 导演， 评分， 评级数量
    :param res:
    :return:
    """
    soup = BeautifulSoup(res.text, 'lxml')
    # 找出tag 为 ol 下的所有子级li标签
    for li in soup.find('ol', class_='grid_view').find_all('li', recursive=True):
        rank = li.find('em').get_text(strip=True)
        a = li.find("div", class_='pic').a
        content_url = a['href']
        title = a.img['alt']
        image_url = a.img['src']
        info = li.find('div').p.get_text(strip=True)
        star = li.find('div', class_='star').find('span', class_='rating_num').get_text(strip=True)
        evaluate_number = li.find('div', class_='star').find_all('span')[-1].get_text(strip=True)
        quote = ''

        # python3.9 最新海象表达式 :=
        if p := li.find('p', class_='quote'):
            quote = p.get_text(strip=True)

        # 排行，内容链接， 标题， 图片链接， 信息， 评分， 评论人数， 引用

        # 生成器
        yield rank, content_url, title, image_url, info, star, evaluate_number, quote

    def find_next(tag):
        if tag.name == 'a' and "后页" in tag.text:
            return True
    next_page = soup.find(find_next)
    if next_page:
        next_page_url = base_url + next_page['href']
        yield next_page_url


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 Safari/537.36 '
    }
    top_urls = [base_url]
    while top_urls:

        # 取出一个链接
        url = top_urls.pop()
        res = request_url(url, headers=headers)
        for data in parse_link(res):
            if isinstance(data, str):
                # 如果是str 就是下一页链接
                top_urls.append(data)
            else:
                print(data)
        # 睡眠5秒 防止被封, 可以设置随机值
        time.sleep(5)


if __name__ == '__main__':
    base_url = "https://movie.douban.com/top250"
    main()
