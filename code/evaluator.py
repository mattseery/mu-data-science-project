#!/usr/bin/python3

import sys
import argparse


def main(ids, output_filename):
    
    
    correct = list()
    incorrect = list()
    for line in sys.stdin:
        id = line.split(';')[0]
        title = line.split(';')[-1]
        if id in ids:
            correct.append("%s\t%s" % (id, title.strip()))
        else:
            incorrect.append("%s\t%s" % (id, title.strip()))

    total = len(correct) + len(incorrect)
    
    accuracy = "{:0.2f}%".format(len(correct)*100 / total,)
    
    
    output = """Accuracy: %s
    
Correct:
%s
    
Incorrect:
%s
""" % (accuracy, "\n".join(correct), "\n".join(incorrect))
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(output)

    print(output)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Breaking News Analysis Evaluator")

    parser.add_argument("-i", "--input", help="Path to list of breaking news ids (including duplicates)", default='breaking-news-ids.txt')
    parser.add_argument("-o", "--output", help="Location of desired output.", default='output.txt')

    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        ids = set(map(str.strip, f.readlines()))
        
    main(ids, args.output)
    