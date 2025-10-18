import datetime
import random
import uuid
from faker import Faker

from data.models import *


def create_test_sindex(faker=None) -> SIndex:
    if faker is None:
        faker = Faker()
    name = faker.word()
    count = random.randint(0,1000)
    score = random.uniform(0,1)
    sindex = SIndex(name, count, score)
    data = {
        'name' : name,
        'count' : count,
        'score' : score
    }
    return sindex, data


def create_test_article() -> Article:
    faker = Faker()

    istopnews = random.randint(0,1) == 0
    doc_id = random.randint(0,1000)
    timestamp = int(datetime.datetime.now().timestamp())
    date_time = datetime.datetime.utcfromtimestamp(timestamp)
    source = faker.company()
    url = faker.url()
    title = faker.sentence()
    content = faker.paragraph(10)
    sindices = list()
    sindices_data = list()
    for _ in range(10):
        sin, sin_d = create_test_sindex(faker)
        sindices.append(sin)
        sindices_data.append(sin_d)

    data = {
        'istopnews' : istopnews,
        'docid' : doc_id,
        'datetime' : timestamp,
        'source' : source,
        'url' : url,
        'title' : title,
        'content' : content,
        'sindices' : sindices_data
    }
    article = Article(doc_id, date_time, istopnews, source, url, title, content, sindices)
    return article, data


def create_test_response(doc_id=None) -> Response:
    faker = Faker()

    if doc_id is None:
        doc_id = random.randint(0,1000)

    keywords = [faker.word()]

    should_publish = random.randint(0,1) == 0
    reason = 'Linguistic' if random.randint(0,1) == 0 else "High Doc Freq"
    tipe = 'Breaking' if random.randint(0,1) == 0 else "Keyword"

    response = Response(doc_id, should_publish, keywords, reason, tipe)
    data = {
        'docid': doc_id,
        'should_publish' : should_publish,
        'keywords': keywords,
        'reason' : reason,
        'tipe' : tipe
    }
    return response, data