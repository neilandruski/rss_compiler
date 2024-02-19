import requests, datetime, article
from rss_parser import Parser

### Constants
STYLE = \
    '<meta charset="UTF-8">\n'\
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'\
    '<title>Security Trough</title>\n'\
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'\
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'\
    '<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono&family=Anton" rel="stylesheet">\n'\
    '<link rel="stylesheet" href="style.css">\n'

SITES = [
    "https://feeds.feedburner.com/TheHackersNews.xml"
    "https://www.bleepingcomputer.com/feed/"
]

FLAGS = ['atlassian',
         'global protect',
         'macos',
         'apple',
         'window',
         'windows 11',
         'microsoft']

### FUNCTIONS
def get_rss_feed(url:str) -> str:
    xml = requests.get(url).text
    return xml

def parse_xml(xml:str) -> [article.Article]: # type: ignore
    articles = []
    rss = Parser.parse(xml)
    for item in rss.channel.items:
        articles.append(article.Article(item.title.content, item.pub_date.content, item.description.content, item.link.content, FLAGS))
    return articles

if __name__ =="__main__":
    html=f'<!DOCTYPE html><head>\n{ STYLE }</head>\n<body>\n'\
        '<div id="bar">\n'\
        '<div><h1>Security Trough</h1><h6>Come get your feed</h6></div>\n'\
        '<div id="sheep"> <img src="sheep.png" alt="Sheep"></div>\n'\
        '</div>\n'\
        '<div class="container">\n'
    articles_list = []
    xml = ''

    for site in SITES:
        xml = get_rss_feed(site)
        articles_list += parse_xml(xml)
    
    for item in articles_list:
         html += item.get_html()

    html += '</div><div id="flock"><img src="sheep_trough.png" alt="Sheep Trough"></div>\n</body>\n'

    with open('index.html', "w") as f:
        f.write(html)