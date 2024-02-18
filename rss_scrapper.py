
### Imports
import requests, hashlib, datetime
from rss_parser import Parser


### Constants
STYLE = \
    '<meta charset="UTF-8">\n'\
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'\
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'\
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'\
    '<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono" rel="stylesheet">\n'\
    '<link href="https://fonts.googleapis.com/css2?family=Bevan" rel="stylesheet">\n'\
    '<link rel="stylesheet" href="style.css">\n'\

SITES = [
    "https://feeds.feedburner.com/TheHackersNews.xml"
    "https://www.bleepingcomputer.com/feed/"
]

FLAGS = ['atlassian',
         'global protect',
         'macOS'
         'windows 11',
         'microsoft']
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
        
        title = f'<h3><a href="{ self.link }" target="_blank">{ self.title }</a></h3>\n'
        date = f'<p class="date">{ self.date[:16] }</p>\n'
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
    
    html=f'<!DOCTYPE html><head>\n{ STYLE }</head>\n<body>\n'\
        '<div id="bar">\n'\
        '<div><h1>Security Trough</h1><h6>Come get your feed</h6></div>\n'\
        '<div id="sheep"> <img src="sheep.png" alt="Sheep"></div>\n'\
        '</div>\n'\
        '<div class="container">\n'
    for article in articles_list:
         html += article.get_html(articles_list.index(article))

    html += '</div><div id="flock"><img src="sheep_trough.png" alt="Sheep Trough"></div>\n</body>\n'

    with open('index.html', "w") as f:
        f.write(html)
    