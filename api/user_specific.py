from newsapi import NewsApiClient


def __api_key():
    key = 'e0d3ec8f0c0140f6b99146bf9e4469d7'
    # key = '657a010b291d44b29c0bea510c097299'
    return key


def personal(sour):
    news_api = NewsApiClient(api_key=__api_key())
    sources_news = news_api.get_top_headlines(sources=sour)
    result = {
        'sources': sources_news['articles'],

    }
    return result
