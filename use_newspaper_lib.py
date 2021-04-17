import newspaper
import requests
from tqdm import tqdm

def set_cnn_url(url):
    r = requests.get(url)
    st = str(r.content)
    artiIndex = st.find('{"articleList":')
    st = st[artiIndex:]
    artiIndex = st.find(", registryURL:")
    st = st[:artiIndex]
    l  = st.split('"uri":"')
    cnn_urls = []
    for x in l:
        htmlStart = x.find('index.html')
        if htmlStart != -1   :
            htmlStart =  htmlStart + len('index.html')  
            cnn_urls.append(url + x[:htmlStart])
    return cnn_urls

def get_content(cnn_urls):
    date_list = []
    text_list = []
    title_list = []
    author_list = []
    for content in cnn_urls:
        content = newspaper.Article(content)
        content.download()
        content.parse()
        author_list.append(" ".join(content.authors))
        date_list.append(content.publish_date)
        text_list.append(content.text)
        title_list.append(content.title)
        break
    return date_list, text_list, title_list, author_list

cnn_urls = set_cnn_url("https://edition.cnn.com")
date_list, text_list, title_list, author_list = get_content(cnn_urls)
print(date_list)
print(title_list)
print(len(date_list), len(title_list), len(text_list), len(author_list))
