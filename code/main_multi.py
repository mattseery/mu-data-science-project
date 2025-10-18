import os
import logging
import argparse
from pexpect import popen_spawn
import signal

from data import DBClient, FileClient, json, Article
from initialization import init
from config import get_config


CLIENT = get_config()['CLIENT']

def main(subproc):
    if CLIENT.lower() == 'db':
        client = DBClient()
    else:
        client = FileClient()
    
    for data in client.get_articles():
        article = Article.fromDict(data)
        text = json.serialize_article(article)
        subproc.sendline(text)

        text = subproc.readline(1).decode().strip()
        
        logging.info('Recived "%s" from subprocess' % text)
        response = json.deserialize_response(text)

        # DocID, Time Stamp of Doc, Processing Time Length (from reading the doc text to push), Keyword
        if 'breaking' in response.keywords:

            doc_id = response.docid

            timestamp = article.datetime.isoformat()
            #duration = int(article['id']) - timestamp
            duration = 0
            keyword = 'breaking'
            output = ",".join([doc_id, str(timestamp), str(duration), keyword])
            print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Breaking News Analysis")
    parser.add_argument("-d", "--debug", help="Turns on debug logging", action="store_true")
    args = vars(parser.parse_args())
    
    init(args['debug'])
    try:
        subproc = popen_spawn.PopenSpawn('python breaking_news.py')
        main(subproc)
    except Exception as ex:
        logging.critical(ex)
        subproc.kill(signal.SIGTERM)
        subproc.wait()
        raise ex
