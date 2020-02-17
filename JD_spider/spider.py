import json
import requests
from lxml import etree
import csv


def get_good_urls(keyword, page):
    p = page * 2 - 1
    good_urls = []
    for it in range(p, p + 2):
        url = "https://search.jd.com/Search?keyword=" + keyword + "&enc=utf-8&qrst=1&rt=1&stop=1&vt=1&stock=1&page=" + str(
            it) + "&s=" + str(1 + (it - 1) * 30) + "&click=0&scrolling=y"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = response.apparent_encoding
        html = etree.HTML(response.text)
        for j in html.xpath('//*[@id="J_goodsList"]/ul/li/div/div[1]/a/@href'):
            if "https" in j:
                good_urls.append(j)
            else:
                good_urls.append("https:" + j)

    goodlist = []
    with open("test.csv", "a", newline="") as csvfile:
        rows = ("商品名称", "商品价格", "商品链接")
        writer = csv.writer(csvfile)
        writer.writerow(rows)

    for i in good_urls:
        goodlist.append(get_information(i))

    return good_urls


def get_price(sid):
    price_url = "https://p.3.cn/prices/mgets?skuIds=" + sid
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.100 Safari/537.36 '
    }
    response = requests.get(price_url, headers=headers, timeout=30)
    response.encoding = response.apparent_encoding
    jsons = json.loads(response.text[0:-1])
    price = jsons[0]['p']
    if price == "-1.00":
        return "商品已售完"
    else:
        return price


def get_information(url):
    temp = url.split('/')[-1]
    sid = temp.split('.')[0]
    headers = {
        'authority': 'list.jd.com',
        'method': 'GET',
        'path': '/' + url.split('/')[-1],
        'scheme': 'https',
        'accept': '/list.html?cat=9987,653,655&page=1&sort=sort_rank_asc&trans=1&JL=6_0_0&callback=jQuery8321329&md=9&l=jdlist&go=0',
        'accept-encoding': 'gzip, deflate, br',
        'accept-encoding': 'gzip, deflate, br',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.encoding = response.apparent_encoding
    html = etree.HTML(response.text)
    goodsname = html.xpath('//*[@id="detail"]/div[2]/div[1]/div[1]/ul[2]/li[1]/text()')
    goodstore = html.xpath('//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]/div/a/text()')
    price = get_price(sid)
    name = str(goodsname[0]).split("：")[1]
    goodlist = [name, price, url]
    goodlist_detail = ["商品：" + name, "价格：" + price, "链接：" + url]
    with open("test.csv", "a", newline="") as csvfile:
        rows = (name, price, url)
        writer = csv.writer(csvfile)
        writer.writerow(rows)
        print(goodlist)


if __name__ == "__main__":
    for i in range(1, 2):
        get_good_urls("ipad", i)
