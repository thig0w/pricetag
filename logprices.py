# -*- coding: utf-8 -*-
import requests
from apscheduler import Scheduler
from apscheduler.triggers.interval import IntervalTrigger
from lxml import html

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

database = [
    # {
    #     "url": "https://www.kabum.com.br/produto/127932/hd-seagate-6tb-ironwolf-nas-3-5-sata-st6000vn001", # noqa: E501
    #     "xpath": '//*[@id="blocoValores"]/div[2]/div[1]/h4',
    #     "desc": "HD Seagate 6tb",
    # },
    # {
    #     "url": "https://www.netshoes.com.br/tenis-nike-precision-vi-masculino-preto-2IC-7496-006", # noqa: E501
    #     "xpath": '//*[@id="buy-box"]/div[3]/div[2]/div/span[1]/strong',
    #     "desc": "Precision 6 black",
    # },
    # {
    #     "url": "https://www.netshoes.com.br/tenis-nike-precision-vi-masculino-preto+branco-2IC-7496-026", # noqa: E501
    #     "xpath": '//*[@id="buy-box"]/div[3]/div[2]/div/span[1]/strong',
    #     "desc": "Precision 6 white",
    # },
    # {
    #     "url": "https://www.netshoes.com.br/tenis-nike-precision-vi-masculino-preto+dourado-2IC-7496-120", # noqa: E501
    #     "xpath": '//*[@id="buy-box"]/div[3]/div[2]/div/span[1]/strong',
    #     "desc": "Precision 6 dourado",
    # },
    # {
    #     "url": "https://www.kabum.com.br/produto/99175/stream-deck-elgato-medio-15-teclas-personalizaveis-de-lcd-usb-integrado-preto-10gaa9901?gclid=Cj0KCQiAuqKqBhDxARIsAFZELmLzYPHLmrtAhhePcNskPXdXBGi80vx9IcmN_KtIU9Ar9WGZnLf2XTkaAgVnEALw_wcB", # noqa: E501
    #     "xpath": '//*[@id="blocoValores"]/div[2]/div[1]/div/h4',
    #     "desc": "Stream deck",
    # },
    {
        "url": "https://www.kabum.com.br/produto/98243/mouse-sem-fio-logitech-mx-vertical-design-ergonomico-para-reducao-de-tensao-muscular-usb-unifying-ou-bluetooth-recarregavel-910-005447",  # noqa: E501
        "xpath": '//*[@id="blocoValores"]/div[2]/div[1]/div/h4',
        "desc": "mx vertical",
    },
    {
        "url": "https://www.decathlon.com.br/jaqueta-masculina-de-corrida-kiprun-rain-kalenji-63379/p",  # noqa: E501
        "xpath": "/html/body/div[1]/div/div[1]/div[2]/div/section/section[2]/div[1]/div[1]/h2",  # noqa: E501
        "desc": "kiprun rain",
    },
]


def execute():
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


if __name__ == "__main__" or __name__ == "__builtin__":
    scheduler = Scheduler()
    scheduler.add_schedule(execute, IntervalTrigger(minutes=1))
    scheduler.start_in_background()
