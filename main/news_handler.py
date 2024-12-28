import requests
from os import environ
from datetime import datetime, timedelta


token = environ['market_aux_api_token']


def get_news_of_last_week(stock_symbol_list):
    if len(stock_symbol_list) == 0 or stock_symbol_list is None:
        return []
    url = 'https://api.marketaux.com/v1/news/all'
    stocks_str = ','.join(stock_symbol_list)
    a_week_ago = get_date_a_week_ago()
    limit = 2  # temporarily
    response = requests.get(f'{url}?symbols={stocks_str}&limit={limit}&filter_entities=true&language=en&api_token={token}&published_after={a_week_ago}')
    return response.json()['data']


def get_date_a_week_ago():
    # Get today's date
    today = datetime.now()
    # Subtract 7 days
    seven_days_ago = today - timedelta(days=7)
    # Return the date in "YYYY-MM-DD" format
    return seven_days_ago.strftime("%Y-%m-%d")


# {'meta': {'found': 394, 'returned': 3, 'limit': 3, 'page': 1},
# 
# 'data': 
# [
    # {'uuid': 'de85322a-8049-40cb-b507-af49a1cfc07e', 
    # 'title': "Elon Musk vows 'war' over H-1B visa program amid rift with some Trump supporters By Reuters", 
    # 'description': "Elon Musk vows 'war' over H-1B visa program amid rift with some Trump supporters", 'keywords': '', 
    # 'snippet': 'By Nandita Bose\n\nWEST PALM BEACH, Florida (Reuters) - Elon Musk, the billionaire CEO of Tesla (NASDAQ: ) and SpaceX, vowed 
    # to go to "war" to defend the H-1B vis...', 
    # 'url': 'https://www.investing.com/news/world-news/elon-musk-vows-war-over-h1b-visa-program-amid-rift-with-some-trump-supporters-3790586', 
    # 'image_url': 'https://i-invdn-com.investing.com/news/LYNXNPEB8T05E_L.jpg', 'language': 'en', 
    # 'published_at': '2024-12-28T18:45:38.000000Z', 'source': 'investing.com', 'relevance_score': None, 
    # 'entities': [{'symbol': 'TSLA', 'name': 'Tesla, Inc.', 'exchange': None, 'exchange_long': None, 'country': 'us', 'type': 'equity',
    # 'industry': 'Consumer Cyclical', 'match_score': 13.044094, 'sentiment_score': 0.175167, 'highlights': 
    # [{'highlight': 'By Nandita Bose\n\nWEST PALM BEACH, Florid[+315 characters]', 'sentiment': 0.0516, 'highlighted_in': 'main_text'}, 
    # {'highlight': 'In a post on social media platform X, Mu[+274 characters]', 'sentiment': 0.296, 'highlighted_in': 'main_text'}, 
    # {'highlight': 'Musk, a naturalized U.S. citizen born in[+224 characters]', 'sentiment': 0.1779, 'highlighted_in': 'main_text'}]}],
    # 'similar': []},
# 
# {'uuid': '555cf97a-4f2f-420d-87b4-459f3b49a780', 
# 'title': 'Elon Musk Doubles Down on Support for German Far-Right Party AfD', 
# 'description': 'Elon Musk reiterated his support for the far-right Alternative for Germany party, or AfD,
# in an opinion piece published by the Welt am Sonntag newspaper less than two months before Germans go to the polls.',
# 'keywords': 'Elon Musk, Alternative for Germany, AfD, immigration policy, German culture', 'snippet': 'Elon Musk reiterated his
# support for the far-right Alternative for Germany party, or AfD, in an opinion piece published by the Welt am Sonntag newspaper less
# th...', 'url': 'https://www.livemint.com/opinion/online-views/elon-musk-doubles-down-on-support-for-german-far-right-party-afd-11735411388419.html',
# 'image_url': 'https://www.livemint.com/lm-img/img/2024/12/18/1600x900/opinion2_1734536366238_1734536388202.jpg', 'language': 'en', 
# 'published_at': '2024-12-28T18:43:07.000000Z', 'source': 'livemint.com', 'relevance_score': None, 'entities': [{'symbol': 'TSLA', 'name': 'Tesla, Inc.', 'exchange': 
# None, 'exchange_long': None, 'country': 'us', 'type': 'equity', 'industry': 'Consumer Cyclical', 'match_score': 15.660858, 'sentiment_score': 0.25, 'highlights': [{'highlight': 'A key adviser to US President-elect Dona[+147 characters]', 'sentiment': 0.25, 'highlighted_in': 'main_text'}]}], 'similar': []},
# 
# {'uuid': 'e58bf3c2-265d-489a-8599-9c9d5e79b69d', 'title': 'A year in wealth: The biggest billionaire winners and losers of 2024', 'description': 'Tech billionaires like 
# Elon Musk and Jeff Bezos saw their fortunes soar in 2024, while the net worths of retail titans like Bernard Arnault took a hit.', 'keywords': 'Bernard Arnault, Elon Musk, Bloomberg Billionaires Index, net worth, Donald Trump', 'snippet': "Bernard Arnault lost more money than any other billionaire this year — while Elon Musk's fortune nearly doubled. Chesnot/Getty Images; Marc Piasecki/Getty Ima...", 'url': 'https://finance.yahoo.com/news/wealth-biggest-billionaire-winners-losers-100701295.html', 'image_url': 'https://s.yimg.com/ny/api/res/1.2/zFySP9yf_of7CE6pjQwC8A--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyMDA7aD05MDA-/https://media.zenfs.com/en/business_insider_articles_888/64c66b8a8d654bbd397edfa68aebcc03', 'language': 'en', 'published_at': '2024-12-28T18:07:01.000000Z', 'source': 'finance.yahoo.com', 'relevance_score': None, 'entities': [{'symbol': 'TSLA', 'name': 'Tesla, Inc.', 'exchange': None, 'exchange_long': None, 'country': 'us', 'type': 'equity', 'industry': 'Consumer Cyclical', 'match_score': 8.85698, 'sentiment_score': 0.5796, 'highlights': [{'highlight': 'His fortune is predominantly made up of [+254 characters]', 'sentiment': 0.5106, 'highlighted_in': 'main_text'}, {'highlight': 'Ellison also owns more than 1% of <em>Te[+195 characters]', 'sentiment': 0.6486, 'highlighted_in': 'main_text'}]}], 'similar': []}]}