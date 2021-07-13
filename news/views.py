from django.db.models.query_utils import subclasses
from django.shortcuts import render, redirect

import requests
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

requests.packages.urllib3.disable_warnings()

def news_list(request):
    headlines = Headline.objects.all()
    context = {
        'object_list':headlines,
    }
    return render(request, "home.html", context)

keywords = ['student', 'study', 'democracy', 'infrastructure', 'game']

def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://www.theonion.com/"
    content = session.get(url, verify=False).content
    soup = BSoup(content, "html.parser")
    News = soup.select("article.sc-1pw4fyi-5.hgZOhx.js_post_item")
    print(len(News))

    Headline.objects.all().delete()

    for article in News:
        main = article.find_all('a')[0]
        image = main.find('img')
        title = article.find_all('h4')[0].contents[0]
        link = main['href']
        image_src = ""
        if image is not None:
            if image.has_attr('srcset'):
                image_src = str(image['srcset']).split(" ")[16]
            elif image.has_attr('data-srcset'):
                image_src = str(image['data-srcset']).split(" ")[16]

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = image_src
        b = False
        for word in keywords:
            if word in title.lower():
                b = True
        if b:
            new_headline.save()
        
    return redirect("/")