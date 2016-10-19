#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    File name: Executor.py
    Author: Marcel Grossmann
    Date created: 6/7/2016
    Date last modified: 6/10/2016
    Python Version: 3.4
'''

from os import remove, listdir, makedirs, path
from subprocess import call
from csv import DictReader

class Configurator:
    def __init__(self, **kwargs):
        self.metaCSV = kwargs['metaCSV']
        self.inTemplate = kwargs['inTemplate']
        self.outTemplate = '%s/%s' % (kwargs['folder'], kwargs['outTemplate'])
        self.main = kwargs['main']
        self.folder = kwargs['folder']
        self.no = 0
        self.line = {}

    def readAssignmentInfo(self, number):
        self.no=number
        metainfo = DictReader(open(self.metaCSV, 'rt', encoding='utf-8'), delimiter=',', quotechar='"')
        for row in metainfo:
            if row['number'] == str(number):
                self.line = row

    def writeTexInfo(self):
        inFile = open(self.inTemplate, 'r', encoding="utf-8")
        temp = inFile.read()
        page = temp % self.line
        makedirs(path.dirname(self.outTemplate), exist_ok=True)
        outFile = open(self.outTemplate, 'w', encoding='utf-8')
        outFile.write(page)

    def runLatex(self):
        call(['latexmk', '-shell-escape', '-synctex=1', '-pdf', self.main], cwd=self.folder)

    def cleanUp(self):
        call(['latexmk', '-C'], cwd=self.folder)
        [remove('%s/%s' % (self.folder, f)) for f in listdir(self.folder) if f.endswith(('.gnuplot', '.table', '.nav', '.snm', '.gz', '.bbl', '.nlo'))]

    def cpResult(self, finalName):
        finalfolder = '../%s%s/' % (self.folder.replace("Template", "").strip(), self.no)
        finalfile = '%s%s.pdf' % (finalName,  '0%i' % self.no if self.no < 10 else self.no)
        call(['cp', self.main.replace('.tex', '.pdf'), '%s%s' % (finalfolder, finalfile)], cwd=self.folder)

from threading import Thread

class Builder(Thread):
    def __init__(self, buildNo, prepend='', **kwargs):
        Thread.__init__(self)
        self.setup=kwargs
        self.number=buildNo
        self.cleanup=False
        self.prepend=prepend

    def setCleanup(self, cleanup=False):
        self.cleanup=cleanup

    def run(self):
        curr = Configurator(**self.setup)
        curr.readAssignmentInfo(self.number)
        curr.writeTexInfo()
        curr.runLatex()
        curr.cpResult(self.prepend)
        if self.cleanup:
            curr.cleanUp()

from re import findall

class Executor():
    def __init__(self, **kwargs):
        threads=[]
        shortterm="\def\@term"
        shortlecture="\def\@lecture"
        pattern="\{(.*?)\}"

        for line in open(kwargs['inTemplate']):
            if shortterm in line:
                term = findall(pattern, line)[0].lower().replace('/','')
            if shortlecture in line:
                lecture = findall(pattern, line)[0].lower()

        if term and lecture is not None:
            print(kwargs)
            term = "%s-%s-%s" % (lecture, term, kwargs['folder'].replace("Template", "").strip())
        else:
            term = "a"
        for i in kwargs['number']:
            build = Builder(i, term, **kwargs)
            if kwargs['clean']:
                build.setCleanup(True)
            threads += [build]
            build.start()
            for x in threads:
                x.join()
