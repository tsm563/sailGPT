from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

blacklist = [
    '[document]',

   'noscript',
    'header',
    'html',
    'meta',
    'head',
    'input',
    'script',
    # there may be more elements you don't want, such as "style", etc.
]

def load_page(url: str) -> [str, str]:
    req = Request("https://{}".format(url), headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    links = [link.get('href') for link in soup.findAll('a')]
    text  = soup.findAll(text=True)
    filtered_text = ''
    for t in text:
        if t.parent.name not in blacklist:
            filtered_text += '{} '.format(t)
    return [filtered_text, links]

to_visit, visited = set(['documentation.sailpoint.com/saas/user-help/getting_started/registering.html']), set()
prefix = "documentation.sailpoint.com"

while to_visit:
    next_page = to_visit.pop()
    text, links = load_page(next_page)
    visited.add(next_page)
    print("VISITED: {}".format(next_page))

    next_page = next_page.replace("https://", "").replace("/", "_")
    with open("source_documents/{}.txt".format(next_page.replace("https://", "")), 'w') as f:
        f.write(text)

    for link in links:
        if link:
            link = link.replace("https://", "")
            if link.startswith(prefix) \
               and link not in to_visit \
               and link not in visited:
                to_visit.add(link)
                print("To Visit: {}".format(link))

    print("Visited: {} --- Remaining: {}".format(len(visited), len(to_visit)))