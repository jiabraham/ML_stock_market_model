#!/usr/local/bin/python3
# coding: utf-8

import sys, getopt
from time import time

import warc
from selectolax.parser import HTMLParser

def get_text_selectolax(html):
    tree = HTMLParser(html)

    if tree.body is None:
        return None

    for tag in tree.css('script'):
        tag.decompose()
    for tag in tree.css('style'):
        tag.decompose()

    text = tree.body.text(separator='\n')
    return text


def read_doc(record, parser=get_text_selectolax):
    url = record.url
    text = None

    if url:
        payload = record.payload.read()
        header, html = payload.split(b'\r\n\r\n', maxsplit=1)
        html = html.strip()

        if len(html) > 0:
            text = parser(html)

    return url, text


def process_warc(file_name, parser=get_text_selectolax, limit=10000):
    warc_file = warc.open(file_name, 'rb')
    t0 = time()
    n_documents = 0
    for i, record in enumerate(warc_file):
        url, doc = read_doc(record, parser)

        if not doc or not url:
            continue

        print("Document = %s", doc)
        
        n_documents += 1

        if i > limit:
            break

    warc_file.close()
    print('Parser: %s' % parser.__name__)
    print('Parsing took %s seconds and produced %s documents\n' % (time() - t0, n_documents))


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('convert_html_to_text.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('convert_html_to_text.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   print('Input file is %s', inputfile)
   print('Output file is %s', outputfile)
   process_warc(inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])

