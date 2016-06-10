#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    File name: PyTex.py
    Author: Marcel Grossmann
    Date created: 6/7/2016
    Date last modified: 6/10/2016
    Python Version: 3.4
'''

from sys import path, stdin
from argparse import ArgumentParser
from json import loads
from copy import deepcopy

path.append('./pythonlib')
from Executor import Executor
from Docker import Builder as ContainerExecutor

def arguments():
    parser = ArgumentParser(description="Install latexmk or Docker and make sure it's in your path, before you start the Builder with the following parameter")
    parser.add_argument("number", nargs='*', help='Input the exercise number(s)', type=int)
    parser.add_argument('-j','--json', help='To parse a JSON file from stdin', action="store_true", required=False)
    parser.add_argument('-c', '--clean', help="Compile and clean temporary files", action="store_true", required=False)
    parser.add_argument('-d', '--dockerized', help="Perform LaTeX compilation inside a container", action="store_true", required=False)
    parser.add_argument('-cn', '--containerName', help="Specify a custom containerName, if docker is enabled", required=False)

    return vars(parser.parse_args())

def setupDictionary(**kwargs):
    meta = {'metaCSV':'metainfo.csv', 'inTemplate':'template.tex', 'outTemplate':'include/wildcards.tex', 'folder':'ExampleTemplate', 'main':'example.tex'}
    data = dict(list(meta.items()) + list(kwargs.items()))
    if data['containerName'] is None:
        data['containerName'] = 'whatever4711/pytex-example'
    return data

def execute(threads, **kwargs):
    if kwargs['dockerized']:
        ce = ContainerExecutor(**kwargs)
        threads += ce.startThreads(threads)
    else:
        Executor(**kwargs)
    return threads

if __name__ == "__main__":
    args = arguments()

    if args['json']:
        args = loads(stdin.read())

    data = setupDictionary(**args)

    threads = []
    threads = execute(threads, **data)
    for x in threads:
        x.join()
