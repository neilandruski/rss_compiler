import requests, json, html, re
from bs4 import BeautifulSoup as bs

### CONSTANTS
SITES = [
    'https://feeds.feedburner.com/TheHackersNews.xml',
    'https://www.theregister.com/security/headlines.atom',
    'https://www.bleepingcomputer.com/feed/'
]
#https://www.csoonline.com/in/index.rss
#https://feeds.feedburner.com/securityweek
#http://krebsonsecurity.com/feed/
#https://threatpost.com/feed/
#https://www.darkreading.com/rss/all.xml
#https://feeds.feedburner.com/TheHackersNews
#https://www.theregister.com/security/headlines.atom
#https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml
#https://www.bleepingcomputer.com/feed/
#https://www.infosecurity-magazine.com/rss/news


FLAGS = ['atlassian',
         'global protect',
         'macos', 'apple',
         'windows', 'windows 11', 'microsoft']

### FUNCTIONS
def has_flag(content:str) -> bool:
    if (FLAGS is None): return False
    for word in FLAGS:
        if( word in content.lower()):
            return True
    return False


def get_rss_feed(url:str) -> str:
    xml = requests.get(url).text
    return xml


def parse_xml(xml:str) -> [dict]: # type: ignore
    description = 'description'
    date_field = 'pubDate'
    articles = []
    flagged:bool = False
    soup = bs(xml, 'xml')
    site_name = soup.find('title').string
    rss_feed = soup.find_all('item')
    if ( not rss_feed ): 
        rss_feed = soup.find_all('entry')
        description = 'summary'
        date_field = 'published'

    for item in rss_feed:
        flagged = has_flag(item.find('title').string + ' ' + item.find(description).string)
        if item.find('link').string is None: 
            link = item.find('link')['href']
        else:
            link = item.find('link').string 
        desc = re.sub('<[^<]+?>', '', html.unescape(item.find(description).string))
        articles.append({'title': item.find('title').string,
                         'site': site_name,
                         'date': item.find(date_field).string,
                         'description': desc,
                         'link': link,
                         'flag': flagged})
    return articles


def get_articles(sites:[str] = None): # type: ignore
    if sites is None: sites = SITES
    articles_list = []
    for site in SITES:
        articles_list += parse_xml(get_rss_feed(site))

    data = json.dumps(articles_list)
    return data


if __name__ =='__main__':
    articles_list = []
    for site in SITES:
        articles_list += parse_xml(get_rss_feed(site))

    #articles_sorted = sorted(articles_list, key= lambda kv: kv['date'], reverse=True )
    data = json.dumps(articles_list)
    with open('static/src/site.json', 'w') as f:
        f.write(data)
