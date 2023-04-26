# -*- coding: utf-8 -*-
import requests
from lxml import html

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

database = [
    {
        "url": "https://www.kabum.com.br/produto/127932/hd-seagate-6tb-ironwolf-nas-3-5-sata-st6000vn001",
        "xpath": '//*[@id="blocoValores"]/div[2]/div[1]/h4',
        "desc": "HD Seagate 6tb",
    },
    {
        "url": "https://www.netshoes.com.br/tenis-nike-precision-vi-masculino-preto-2IC-7496-006",
        "xpath": '//*[@id="buy-box"]/div[3]/div[2]/div/span[1]/strong',
        "desc": "Precision 6 black",
    },
    {
        "url": "https://www.netshoes.com.br/tenis-nike-precision-vi-masculino-preto+branco-2IC-7496-026",
        "xpath": '//*[@id="buy-box"]/div[3]/div[2]/div/span[1]/strong',
        "desc": "Precision 6 white",
    },
    {
        "url": "https://www.netshoes.com.br/tenis-nike-precision-vi-masculino-preto+dourado-2IC-7496-120",
        "xpath": '//*[@id="buy-box"]/div[3]/div[2]/div/span[1]/strong',
        "desc": "Precision 6 dourado",
    },
]

for i in database:
    # Request the page
    page = requests.get(i["url"], headers=headers)

    # Parsing the page
    # (We need to use page.content rather than
    # page.text because html.fromstring implicitly
    # expects bytes as input.)
    tree = html.fromstring(page.content)

    # Get element using XPath
    price = tree.xpath(i["xpath"])
    try:
        print(f"{i['desc']} - {price[0].text}")
    except IndexError:
        print(f"{i['desc']} - out of stock")
