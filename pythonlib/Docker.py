#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    File name: Docker.py
    Author: Marcel Grossmann
    Date created: 6/7/2016
    Date last modified: 6/10/2016
    Python Version: 3.4
'''

from os import getuid, getgid, getcwd
from subprocess import call, Popen, PIPE
from threading import Thread
from json import dumps

class Docker(Thread):
    def __init__(self, buildNo, **kwargs):
        Thread.__init__(self)
        self.number = buildNo
        self.containerName = kwargs['containerName']
        self.folder = kwargs['folder'].replace("Template", "").strip()
        self.mounted = '%s/%s%i:/pytex/%s%i' % (getcwd(), self.folder, self.number, self.folder, self.number)
        self.data=kwargs
        self.data['dockerized']=False

    def run(self):
        pytex = "echo '%s' | /pytex/PyTex.py -j" % dumps(self.data)

        call(['docker', 'run', '-it', '--rm', '-v', self.mounted,  self.containerName, pytex], cwd=".")
        # Fixing Permissions
        call(['sudo', 'chown', '-R', "%i:%i" % (getuid(), getgid()), "%s/%s%i" % (getcwd(), self.folder, self.number) ])

class Builder():
    def __init__(self, threads=[], **kwargs):
        # Check if container exists
        (output, err) = Popen(["docker", "images"], stdout=PIPE).communicate()
        lines = output.decode('utf-8')
        if str(kwargs['containerName']) not in lines:
            call(['docker', 'build', '-t', kwargs['containerName'], '.'], cwd=".")
        self.data = kwargs

    def startThreads(self, threads=[]):
        for i in self.data['number']:
            dock = Docker(i, **self.data)
            threads += [dock]
            dock.start()

        return threads