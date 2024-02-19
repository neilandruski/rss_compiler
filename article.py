import datetime, hashlib

class Article:
    UID:hex = ""
    title:str = ""
    date:datetime = ""
    description:str = ""
    link:str = ""
    flag:bool = False

    def __init__(self, title, date, description, link, flags = None):
        self.title = title
        self.date = date
        self.description = description
        self.link = link
        self.UID = hashlib.sha256(title.encode()).hexdigest()
        self.flag = self.has_flag(flags)
        
    def has_flag(self, flags:[str]= None) -> bool:
        if (flags == None): return False
        for word in flags:
            if( word in self.description.lower() or word in self.title.lower()):
                return True
        return False
    
    def get_date(self) -> str:
        print(self.date)
        print(type(self.date))
        return self.date

    def get_html(self, number:int = None) -> str:
        tag:str = 'item '
        if( number != None ): tag += f'item-{ number + 1 } '
        if(self.flag): tag +="flag"
        title = f'<h3><a href="{ self.link }" target="_blank">{ self.title }</a></h3>\n'
        date = f'<p class="date">{ self.date[:16] }</p>\n'
        body = f'<p>{ self.description }...</p>\n' 
        block = f'<article class="{ tag }">{ title }{ date }{ body }</article>\n'
        return block