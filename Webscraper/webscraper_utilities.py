from html.parser import HTMLParser
from urllib.request import urlopen


class HTMLImageParser(HTMLParser):
    image_urls = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for attr in attrs:
                attr_name, attr_value = attr
                if attr_name == "src":
                    self.image_urls.append(attr_value)


def get_image_urls(url):
    parser = HTMLImageParser()
    with urlopen(url) as html_file:
        html_data = html_file.read().decode("utf-8")
        parser.feed(html_data)
        image_urls = []
        for image_url in parser.image_urls:
            image_url = image_url.replace("'", "")
            if image_url.endswith("jpg") or image_url.endswith("png"):
                if not image_url.startswith("http"):
                    image_url = "https:" + image_url
                image_urls.append(image_url)

    return image_urls
