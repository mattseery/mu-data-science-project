import os
import logging
import argparse
from pexpect import popen_spawn
import signal

from data import DBClient, json, Article, FileClient
from initialization import init
from config import get_config
from processors import ArticleProcessor


CLIENT = get_config()['CLIENT']

def main():
    if CLIENT.lower() == 'db':
        client = DBClient()
    else:
        client = FileClient()
    
    if get_config()['MODE'] == 'BreakingNews':
        proc = ArticleProcessor()
    else:
        proc = ArticleProcessor(get_config()['KEYWORDS'])
    for data in client.get_articles():
        article = Article.fromDict(data)

        response = proc.process(article)

        
        # DocID, Time Stamp of Doc, Processing Time Length (from reading the doc text to push), Keyword
        if response.should_publish:
            doc_id = response.docid
            tipe = 'Breaking'
            timestamp = article.datetime.isoformat()
            output = ";".join([doc_id, response.tipe, response.reason, ','.join(response.keywords), article.title])
            print(output)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Breaking News Analysis")

    parser.add_argument('-q', "--quick", help="Skips cpu intensive operations to get a quick but approximate result", type=bool, choices=[True, False])

    parser.add_argument('-m', "--mode", help="The mode to run on the articles.", choices=['BreakingNews', 'Keywords'])

    parser.add_argument("-c", "--config", help="Path to yaml configuration file. Default: 'config.yml'", default='config.yml')

    parser.add_argument("-bt", "--breaking_threshold", help="The threshold used to determine if an article is breaking news.", type=float)
    parser.add_argument("-dt", "--duplicate_threshold", help="The threshold used to determine if two articles are duplicates.", type=float)

    parser.add_argument('-kw', '--keywords', metavar='KW', type=str, nargs='+',
                    help='Keywords to run process')

    parser.add_argument("-d", "--debug", help="Turns on debug logging", action="store_true")
    parser.add_argument("-s", "--storage", help="The method used to store temprory data.", choices=['File', 'Mongo'])
    parser.add_argument("-sd", "--snippets_dir", help="Path of directory which contains raw article snippets")
    parser.add_argument("-ld", "--log_dir", help="Path of directory where logs will be stored.")

    parser.add_argument("--db_host", help="IP Address of the MongoDB host (ignored unless Mongo is passed as -s argument)")
    parser.add_argument("--db_port", help="Port used to communicate with MongoDB (ignored unless Mongo is passed as -s argument)")
    parser.add_argument("--db_name", help="Name of the MongoDB collection (ignored unless Mongo is passed as -s argument)")
    args = vars(parser.parse_args())

    config = get_config(args['config'])


    if args['quick']:
        config['QUICK'] = args['quick']

    if args['mode']:
        config['MODE'] = args['mode']

    if args['keywords']:
        config['KEYWORDS'] = args['keywords']

    if args['duplicate_threshold']:
        config['DUPLICATE_DIFFERENCE_THRESHOLD'] = args['duplicate_threshold']

    if args['breaking_threshold']:
        config['BREAKING_THRESHOLD'] = args['breaking_threshold']


    if args['log_dir']:
        config['LOG_DIR'] = args['log_dir']
    if args['snippets_dir']:
        config['DEFAULT_DATA_PATH'] = args['snippets_dir']

    if args['storage']:
        config['CLIENT'] = args['storage']

    if args['db_host']:
        config['DB']['HOST'] = args['db_host']
    if args['db_port']:
        config['DB']['PORT'] = args['db_port']
    if args['db_name']:
        config['DB']['DB'] = args['db_name']


    if args['debug']:
        config['DEBUG'] = True

    init(config['DEBUG'])
    try:
        main()
    except Exception as ex:
        logging.critical(ex)
        raise ex
