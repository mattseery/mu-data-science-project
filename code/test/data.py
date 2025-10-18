import unittest

import data
from data import xml, json
from data.models import *
from datetime import datetime

import test.utils as t_utils


class TestJson(unittest.TestCase):


    def test_serialize_article(self):
        istopnews = False
        doc_id = 905
        timestamp = 1520190071
        date_time = datetime.utcfromtimestamp(timestamp)
        
        source = 'SMH'
        url = "www.smh.com/1"
        title = 'the title'
        content = '''the content
with a newline character in it'''
        sindices = [SIndex('a', 1,1)]
        article = Article(doc_id, date_time, istopnews, source, url, title, content, sindices)

        expected_statments = [
            '"istopnews": false',
            '"docid": 905',
            '"datetime": 1520190071',
            '"source": "SMH"',
            '"url": "www.smh.com/1"',
            '"title": "the title", "content":',
            '"the content\\nwith a newline character in it"',
            '"sindices": [{"name": "a", "count": 1, "score": 1}]'
        ]

        result = data.json.serialize_article(article)
        for expected in expected_statments:
            self.assertIn(expected, result)
        

    def test_deserialize_article(self):
        text = '''{"istopnews": false, "docid": 905, "datetime": 1520190071, "source": "SMH", "url": "www.smh.com/1", "title": "the title", "content": "the content\\nwith a newline character in it", "sindices": [{"name": "a", "count": 1, "score": 1}]}'''
        result = data.json.deserialize_article(text)

        istopnews = False
        doc_id = 905
        date_time = datetime.utcfromtimestamp(1520190071)
        source = 'SMH'
        url = "www.smh.com/1"
        title = 'the title'
        content = '''the content
with a newline character in it'''
        sindices = [SIndex('a', 1,1)]
        expected = Article(doc_id, date_time, istopnews, source, url, title, content, sindices)

        
        self.assertEqual(expected, result)


    def test_serialize_response(self):
        doc_id = 905
        
        
        keywords = ['breaking']
        response = Response(doc_id, True, keywords)

        expected_statments = [
            '"docid": 905',
            '"keywords": ["breaking"]'
        ]

        result = data.json.serialize_response(response)
        for expected in expected_statments:
            self.assertIn(expected, result)


    def test_deserialize_response(self):
        text = '''{"docid": 905, "should_publish": false, "keywords": ["breaking"], "reason": null, "tipe": "Breaking"}'''
        result = data.json.deserialize_response(text)
        doc_id = 905
        keywords = ['breaking']
        expected = Response(doc_id, False, keywords)

        
        self.assertEqual(expected, result)


    def test_article_to_dict(self):
        article, article_data = t_utils.create_test_article()
        expected = article_data
        result = article.toDict()

        self.assertIsInstance(result['datetime'], (float, int))
        self.maxDiff = None
        self.assertEqual(expected, result)

    def test_article_from_dict(self):
        article, article_data = t_utils.create_test_article()

        # gets all of the variables from both objects
        expected = vars(article)

        result = vars(Article.fromDict(article_data))
        self.assertIsInstance(result['datetime'], datetime)
        self.assertEqual(expected, result)


    def test_response_to_dict(self):
        response, response_data = t_utils.create_test_response()
        expected = response_data
        result = response.toDict()

        self.assertEqual(expected, result)

    def test_response_from_dict(self):
        response, response_data = t_utils.create_test_response()

        # gets all of the variables from both objects
        expected = vars(response)
        result = vars(Response.fromDict(response_data))
        
        self.assertEqual(expected, result)


    def test_sindex_to_dict(self):
        sindex, sindex_data = t_utils.create_test_sindex()
        expected = sindex_data
        result = sindex.toDict()

        self.assertEqual(expected, result)

    def test_sindex_from_dict(self):
        sindex, sindex_data = t_utils.create_test_sindex()

        # gets all of the variables from both objects
        expected = vars(sindex)
        result = vars(SIndex.fromDict(sindex_data))
        
        self.assertEqual(expected, result)


class TestXml(unittest.TestCase):

    def test_parse_snippet(self):
        xml_string = """<?xml version="1.0" encoding="utf-8"?>
<snippet>
  <docid>4651397578105122424</docid>
  <date>30/07/2017</date>
  <time>21:08</time>
  <isTopNews>false</isTopNews>
  <source>The Age</source>
  <url>http://www.bankingday.com/nl06_news_selected.php?act=2&stream=70&selkey=22686&hlc=2&hlw=</url>
  <title>Carbon emissions</title>
  <content>A new technique Foundation
AM & PM Update Newsletter
</content>
  <sindexList>
    <sindex>
      <name>Photo asd</name>
      <count>1</count>
      <score>-1</score>
    </sindex>
    <sindex>
      <name>Thursday</name>
      <count>1</count>
      <score>1.1</score>
    </sindex>
  </sindexList>
</snippet>
"""

        result = xml.parse_snippet(xml_string)


        expected_local_time = datetime(2017, 7, 30, 21, 8)

        expected_timestamp = calendar.timegm(expected_local_time.utctimetuple())
        expected = {
            'content': 'A new technique Foundation\nAM & PM Update Newsletter\n',
            'date': '30/07/2017',
            'datetime': expected_timestamp,
            'docid': '4651397578105122424',
            'istopnews': False,
            'source': 'The Age',
            'time': '21:08',
            'title': 'Carbon emissions',
            'url': 'http://www.bankingday.com/nl06_news_selected.php?act=2&stream=70&selkey=22686&hlc=2&hlw=',
            'sindices': [
                    {'count': 1, 'name': 'Photo asd', 'score': -1.0},
                    {'count': 1, 'name': 'Thursday', 'score': 1.1}
                ]
            }

        self.assertEqual(expected, result)


    def test_parse_snippet_with_no_keywords(self):
        xml_string = """<?xml version="1.0" encoding="utf-8"?>
<snippet>
  <docid>4651398140745845073</docid>
  <date>30/07/2017</date>
  <time>23:19</time>
  <isTopNews>false</isTopNews>
  <source>Townsville Bulletin</source>
  <url>http:/3</url>
  <title>Bright spark creates food from nowhere</title>
  <content>
Originally published as
</content>
  <sindexList>
  </sindexList>
</snippet>
"""

        result = xml.parse_snippet(xml_string)
        
        expected_local_time = datetime(2017, 7, 30, 23, 19)
        expected_timestamp = calendar.timegm(expected_local_time.utctimetuple())

        expected = {
            'docid': '4651398140745845073',
            'date': '30/07/2017',
            'time': '23:19',
            'datetime': expected_timestamp,
            'istopnews': False,
            'source': 'Townsville Bulletin',
            'url': 'http:/3',
            'title': 'Bright spark creates food from nowhere',
            'content': '\nOriginally published as\n',
            'sindices': []
            }

        self.assertEqual(expected, result)

