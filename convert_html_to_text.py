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
