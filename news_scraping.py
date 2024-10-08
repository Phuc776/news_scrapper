from newscatcher import Newscatcher
import json

nyt = Newscatcher(website='nytimes.com')
results = nyt.get_news()

raw_articles = results['articles']

filtered_articles = []

count = 0
for article in raw_articles[:10]:
    count += 1
    filtered_article = {
        'count': count,
        'title': article.get('title'),
        'link': article.get('link'),
        'authors': [author.get('name') for author in article.get('authors', [])],
        'published': article.get('published'),
        'main_author': article.get('author'),
        'summary': article.get('summary'),
        'tags': [tag.get('term') for tag in article.get('tags', [])]
    }
    filtered_articles.append(filtered_article)

print(json.dumps(filtered_articles, indent=2))