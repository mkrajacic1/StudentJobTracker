import unicodedata
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def get_text(self) -> str:
        return ' '.join(self.parts)

def extract(html: str) -> str:
    parser = MyHTMLParser()
    parser.feed(html)
    text = parser.get_text()
    text = unicodedata.normalize("NFC", text)
    text = ' '.join(text.split())
    return text