import os
import json
import random
import requests
import wikipedia
from tqdm import tqdm

class WikiInterface:
    def __init__(self):
        if not os.path.exists("articles.json"):
            self.getTopViews(limit=150)

    def openJson(self, path):
        "open a json file"
        with open(path,'r',encoding='utf-8') as f:
            data = json.load(f)
        return data

    
    def writeJson(self, path,data):
        "create a json file"
        with open(path,"w",encoding='utf-8') as f:
            json.dump(data,f,indent=4,ensure_ascii=False)


    def getPage(self, title):
        "return the page content of an article in a dedicated wikipedia object"
        page = wikipedia.page(title,auto_suggest=False)
        return page


    def filterArticles(self, articles):
        "keep only articles with an image and a content"
        kept_articles = [] #with images
        for article in tqdm(articles):
            try:
                a = self.getPage(article["article"])
                entry = {
                    "title":a.title,
                    #"summary":a.summary,
                    "content":a.content.strip(),
                    "image":a.images[0]
                }
                if len(a.images) != 0 and len(a.content) != 0:
                    kept_articles.append(entry)
            except:
                continue
        return kept_articles

    def getTopViews(self, project="en.wikipedia.org", access="all-access", year="2025", month="08", limit=50):
        "saves in a json file the N articles with the most views in wikipedia"
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/{project}/{access}/{year}/{month}/all-days"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (platform; rv:gecko-version) Gecko/gecko-trail Firefox/firefox-version"})
        r.raise_for_status()
        data = r.json()
        articles = data["items"][0]["articles"][:limit]
        articles = self.filterArticles(articles)
        self.writeJson(f"articles.json",articles)


    def get_random_page(self):
        return self.openJson(f"articles.json")
        #print(random_article["title"])