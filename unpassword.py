#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import mechanize
from bs4 import BeautifulSoup
import rarfile

br = mechanize.Browser()
rootdir = u"~/remote/RAID/Downloads/newpctfinished"

def unrar(dpath, xpath, password):
    with rarfile.RarFile(dpath) as opened_rar:
        opened_rar.setpassword(password)
        opened_rar.extractall(xpath)

childdirs = [x[0] for x in os.walk(rootdir)]
for d in childdirs:
    os.chdir(d)
    childfiles = [f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]
    contra = None
    for f in childfiles:
        if 'CONTRASE' in f:
            contfile = open(os.path.join(d, f))
            for line in contfile:
                if line.startswith('http://'):
                    print line
                    br.open(line)
                    soup = BeautifulSoup(br.response(), "lxml")
                    contra = soup.find('input', {"id": "txt_password"})['value']
    for f in childfiles:
        if f.endswith('.rar'):
           print f
           unrar(f, d, contra)
os.system('/home/maza/remote/RAID/Desarrollo/newpct/renombrar.sh')
