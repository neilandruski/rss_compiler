
### Imports
import requests, hashlib, datetime
from rss_parser import Parser


### Constants
STYLE = \
    '<meta charset="UTF-8">\n'\
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'\
    '<link rel="preconnect" href="https://fonts.googleapis.com">'\
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'\
    '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@100;200;300;400;500;600;700&family=Roboto&display=swap" rel="stylesheet">'\
    '<link rel="stylesheet" href="style.css">\n'\

SITES = [
    "https://feeds.feedburner.com/TheHackersNews.xml"
    "https://www.bleepingcomputer.com/feed/"
]

FLAGS = ['russia']
#DATE = datetime.datetime()

### Class
class Article:
    UID:hex = ""
    title:str = ""
    date:datetime = ""
    description:str = ""
    link:str = ""
    flag:bool = False

    def __init__(self, title, date, description, link):
        self.title = title
        self.date = date
        self.description = description
        self.link = link
        self.UID = hashlib.sha256(title.encode()).hexdigest()
        self.flag = self.has_flag()
        
    def has_flag(self) -> bool:
        for word in FLAGS:
            if( word in self.description.lower() or word in self.title.lower()):
                return True
        return False
    
    def get_date(self) -> str:
        print(self.date)
        print(type(self.date))
        return self.date

    def get_html(self, number:int) -> str:
        tag:str = f'item item-{ number + 1 }'
        if(self.flag): tag +=" flag"
        
        title = f'<h3><a href="{ self.link }">{ self.title }</a></h3>\n'
        date = f'<p><b>{ self.date[:16] }</b></p>\n'
        body = f'<p>{ self.description }...</p>\n' 
        block = f'<article class="{ tag }">{ title }{ date }{ body }</article>\n'
        return block


### Functions

def get_rss_feed(url:str) -> str:
    xml = requests.get(url).text
    return xml

def parse_xml(xml:str) -> [Article]:
    articles = []
    rss = Parser.parse(xml)

    for item in rss.channel.items:

        article = Article(item.title.content, item.pub_date.content, item.description.content, item.link.content)
        articles.append(article)
        
    return articles

if __name__ =="__main__":
    
    articles_list = []

    for site in SITES:
        xml = get_rss_feed(site)
        articles = parse_xml(xml)
        articles_list += articles
    
    html=f'<!DOCTYPE html><head>{ STYLE }</head>\n<body>\n<div id="bar"><h1>Security Trough</h1></div>\n<div class="container">\n'
    for article in articles_list:
         html += article.get_html(articles_list.index(article))

    html += '</div>\n</body>\n'

    with open('index.html', "w") as f:
        f.write(html)
    