import re
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.in_body = False
        self.tags_to_ignore = {'script', 'style', 'nav', 'footer', 'header'}
        self.skip_depth = 0
        self.current_tag = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
        
        if tag in self.tags_to_ignore:
            self.skip_depth += 1
            
        if self.skip_depth == 0 and self.in_body:
            attr_dict = dict(attrs)
            if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(tag[1])
                self.output.append(f"\n{'#' * level} ")
            elif tag == 'img':
                src = attr_dict.get('src', '')
                alt = attr_dict.get('alt', 'image')
                if src:
                    self.output.append(f"\n![{alt}]({src})\n")
            elif tag == 'a':
                href = attr_dict.get('href', '')
                self.output.append(f" [link]({href}) ")
            elif tag == 'p':
                self.output.append("\n\n")
            self.current_tag = tag

    def handle_endtag(self, tag):
        if tag in self.tags_to_ignore:
            if self.skip_depth > 0:
                self.skip_depth -= 1
        if self.skip_depth == 0 and self.in_body:
            if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']:
                self.output.append("\n")

    def handle_data(self, data):
        if self.skip_depth == 0 and self.in_body:
            text = data.strip()
            if text:
                self.output.append(text + " ")

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = MyHTMLParser()
    parser.feed(content)
    
    # clean up blank lines
    text = "".join(parser.output)
    clean_text = re.sub(r'\n\s*\n', '\n\n', text)
    
    with open('murtaza_content.md', 'w', encoding='utf-8') as f:
        f.write(clean_text)

if __name__ == '__main__':
    parse_html('murtaza_scrape.html')
