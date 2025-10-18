import logging

from processors import ArticleProcessor
from data import json
from initialization import init_logging

def main():
    proc = ArticleProcessor()

    while True:
        text = input()
        
        article = json.deserialize_article(text)
        logging.info('Recived "%s" from subprocess' % article.docid)

        resp = proc.process(article)
        text = json.serialize_response(resp)

        logging.info('Sending "%s" to main process' % text)
        print(text, end='\r\n')

        


if __name__ == '__main__':    
    init_logging(True, True)
    main()

