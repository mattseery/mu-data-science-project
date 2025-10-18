import os
import unittest
from datetime import datetime


from data import Article, Response
from data.json import deserialize_article
from processors import ArticleProcessor
import test.utils as t_utils


class TestArticleProcessor(unittest.TestCase):

    @staticmethod
    def load_file(filename):
        filepath = os.path.join('test', filename)
        with open(filepath, encoding='utf-8') as f:
            return list(map(deserialize_article, f.readlines()))

    @classmethod
    def setUpClass(cls):
        cls.related_articles = cls.load_file('related_articles.json')
        cls.unique_articles = cls.load_file('unique_articles.json')
        cls.duplicate_articles = cls.load_file('duplicate_articles.json')

    def test_response(self):
        
        proc = ArticleProcessor()

        article, _ = t_utils.create_test_article()

        resp = proc.process(article)
        self.assertIsInstance(resp, Response)
        self.assertIsInstance(resp.docid, int)
        self.assertIsInstance(resp.keywords, list)

        self.assertEqual(article.docid, resp.docid)


    def test_dont_publish_random(self):
        proc = ArticleProcessor()
        articles = [t_utils.create_test_article()[0] for _ in range(5)]
        for article in articles:
            resp = proc.process(article)
            self.assertFalse(resp.should_publish)



    def test_large_publish_test(self):
        proc = ArticleProcessor()
        articles = [t_utils.create_test_article()[0] for _ in range(15)]
        for article in articles:
            article.datetime = datetime.now()
        for article in articles:
            resp = proc.process(article)
            self.assertFalse(resp.should_publish)



    def test_publish_breaking_article(self):
        proc = ArticleProcessor()
        article = t_utils.create_test_article()[0]
        article.content = "breaking more to come"
        
        self.assertTrue(proc._article_score(article))


    def test_publish_one_breaking_article(self):
        proc = ArticleProcessor()
        article = t_utils.create_test_article()[0]
        article.content = "breaking more to come"
        articles = [article, article, article]

        resp = proc.process(article)
        self.assertTrue(resp.should_publish)

        for a in articles:
            resp = proc.process(a)
            self.assertFalse(resp.should_publish)


    def test_is_duplicate_real_data(self):        
        target = self.duplicate_articles[0]
        articles = self.duplicate_articles[1:]
        self.assertTrue(ArticleProcessor.is_duplicate(target, articles))


    def test_is_not_duplicate_real_data(self):
        target = self.unique_articles[0]
        articles = self.unique_articles[1:]
        self.assertFalse(ArticleProcessor.is_duplicate(target, articles))


    def test_is_related_real_data(self):        
        target = self.related_articles[0]
        articles = self.related_articles[1:]

        result = ArticleProcessor.get_related(target, articles)
        self.assertEquals(len(result), 1)

    def test_is_duplicate_simple(self):
        articles = [t_utils.create_test_article()[0] for _ in range(5)]
        target = t_utils.create_test_article()[0]

        self.assertFalse(ArticleProcessor.is_duplicate(target, articles))

        target = articles[0]

        self.assertTrue(ArticleProcessor.is_duplicate(target, articles))


    def test_is_duplicate_with_added_words(self):
        articles = [t_utils.create_test_article()[0] for _ in range(5)]
        target = t_utils.create_test_article()[0]

        self.assertFalse(ArticleProcessor.is_duplicate(target, articles))

        target = Article.fromDict(articles[0].toDict())
        target.content += " small difference"

        self.assertTrue(ArticleProcessor.is_duplicate(target, articles))


    def test_is_duplicate_with_empty_list(self):
        target = t_utils.create_test_article()[0]
        self.assertFalse(ArticleProcessor.is_duplicate(target, []))
