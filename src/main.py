# -*- coding: utf-8 -*-
##------------ remove
import requests
from apscheduler import Scheduler
from apscheduler.triggers.interval import IntervalTrigger
from lxml import html

from src.pricetag import create_app

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
database = [
    {
        "url": "https://www.kabum.com.br/produto/98243/mouse-sem-fio-logitech-mx-vertical-design-ergonomico-para-reducao-de-tensao-muscular-usb-unifying-ou-bluetooth-recarregavel-910-005447",  # noqa: E501
        "xpath": '//*[@id="blocoValores"]/div[2]/div[1]/div/h4',
        "desc": "mx vertical",
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


scheduler = Scheduler()
scheduler.add_schedule(execute, IntervalTrigger(minutes=1))
# scheduler.start_in_background()
##------------ end remove

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
