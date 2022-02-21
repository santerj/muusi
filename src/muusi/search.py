import re
import requests

from bs4 import BeautifulSoup
from time import sleep


class Search:

    def __init__(self, url) -> None:
        self.baseurl = "https://muusikoiden.net"
        self.url = url
        self.ads = []
        self._get_ads()  
        self.result = []

        for ad in self.ads:
            self.result.append(self.parse_ad(ad))
            sleep(0.05) # sleep 50 ms

    def _get_ads(self) -> list[str]:
        valid = re.compile("\/tori\/ilmoitus\/[0-9]+$")
        offset = 0
        offset_increment = 15
        results = []

        while True:
            url = self.url + f"&offset={offset}"
            document = requests.get(url=url).text
            soup = BeautifulSoup(document, "html.parser")
            tags = soup.find_all("a")
            paginate = False

            for tag in tags:
                try:
                    href = tag["href"]
                    if valid.match(href):
                        url = self.baseurl + href
                        results.append(url)
                        paginate = True
                except KeyError:
                    continue

            if paginate:
                offset += offset_increment
                sleep(0.05)  # sleep for 50 ms to avoid rate limit
            else:
                break

        self.ads = results


    def parse_ad(self, url) -> dict:
        """
        Hacky parsing of muusikoiden.net HTML
        """
        this = Ad()
        this.link = url
        document = requests.get(url=url).text
        soup = BeautifulSoup(document, "html.parser")

        # parse ad details.
        parts = soup.find_all("td", {"class": "tori_title"})[0].text.split(":")  # split type and title
        this.type = parts[0]
        this.title = parts[1].strip()
        this.text = soup.find_all("font", {"class": "msg"})[0].text.replace("\r", "")

        # find added and expiry dates
        tags = soup.find_all("small", {"class": "light"})
        parts = tags[0].text.strip().rstrip().split()
        this.created = parts[1]  # DD.MM.YYYY
        this.expires = parts[3]  # DD.MM.YYYY

        # try to find images
        tags = soup.find_all("a", {"class": "nohover"})
        for tag in tags:
            try:
                if "/dyn/tori/" in tag["href"]:
                    this.images.append(self.baseurl + tag["href"])
            except KeyError:
                continue

        # try to find price
        tags = soup.find_all("p")
        for tag in tags:
            if "Hinta: " in tag.text:
                parts = tag.text.split(":")  # remove "Hinta:" prefix
                this.price = parts[1].strip()

        # find category
        tags = soup.find_all("td", {"colspan": "2"})
        for tag in tags:
            if "Osasto:" not in tag.text:
                continue
            asd = tag.find("a")
            if asd:
                this.category = asd.text
                break

        # find location
        tags = soup.find_all("td", {"colspan": "2"})
        for tag in tags:
            if "Osasto" not in tag.text:
                continue
            parts = str(tag).split("<br/>")
            for part in parts:
                if "Paikkakunta" in part:
                    this.location = part[part.find("</b>")+4:].strip()

        return this.as_dict()


class Ad:

    def __init__(self) -> None:
        self.link:     str
        self.type:     str
        self.title:    str
        self.text:     str
        self.category: str
        self.location: str
        self.price =   "None"
        self.images =  []    # array of image URLs
        self.added:    str   # DD.MM.YYYY
        self.expires:  str   # DD.MM.YYYY

    def as_dict(self):
        payload = {
            "link": self.link,
            "type": self.type,
            "title": self.title,
            "text": self.text,
            "category": self.category,
            "location": self.location,
            "price": self.price,
            "images": self.images,
            "created": self.created,
            "expires": self.expires
        }
        return payload
