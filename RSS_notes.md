
# RRS feed digestor

- have a list of rss feeds URLs
- Have a list of important keywords
- Parse the XML for todays items
- Build items to display
    - struct
        - UID -> sha256 of title
        - Title
        - Description
        - Link
        - FLAG?? - adds a "class" to the html css to 
    - Methods
        - new
        - get_html
        - 

## Note from machine

### html format
Head
style -> baked css style
/head
body
    H1 -> Daily report
        loop through
        { 
        Div class -> FLAG odd|even item
            h2 -> title -> is a -> link
            p -> author
            p -> description
        }

get_html func (number int) -> str:
    title = f"<h2><a href="{link}">{title}</a></h2>\n"
    body = f"<p>{descripton}</p>"
    alt_tag = if(number % 2)? 
    block = f"<div class="{ FLAG } { alt_tag }">{ title }{ body }<div>"
