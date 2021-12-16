from newsapi import NewsApiClient


def __api_key():
    key = '6eaaeea77bc84fec8f763539beb23d31'
    # key = ''
    return key


def get_all():
    news_api = NewsApiClient(api_key=__api_key())
    top_headlines = news_api.get_top_headlines(sources='bbc-news,abc-news,the-verge', page_size=30)
    return top_headlines


def category(cat, qty):
    news_api = NewsApiClient(api_key=__api_key())
    news_category = news_api.get_top_headlines(category=cat, page_size=qty, language='en')
    return news_category


def sources(sou, qty):
    news_api = NewsApiClient(api_key=__api_key())
    news_sources = news_api.get_top_headlines(sources=sou, page_size=qty, language='en')
    return news_sources


def get_source():
    news_api = NewsApiClient(api_key=__api_key())
    news_sources = news_api.get_sources()
    return news_sources['sources']


def query(keyword):
    news_api = NewsApiClient(api_key=__api_key())
    data = news_api.get_everything(q=keyword)
    return data


def source_selected(source_name):
    news_api = NewsApiClient(api_key=__api_key())
    try:

        data = news_api.get_top_headlines(sources=source_name, page_size=30,language='en')
        if data:
            return data['articles']
        else:
            return False
    except Exception:
        return False


def category_selected(category_name):
    news_api = NewsApiClient(api_key=__api_key())
    data = news_api.get_top_headlines(category=category_name,page_size=30,language='en')
    if data:
        return data['articles']
    else:
        return False

def language_selected(language_id):
    news_api = NewsApiClient(api_key=__api_key())
    data = news_api.get_top_headlines(language=language_id)
    if data:
        return data['articles']
    else:
        return None

