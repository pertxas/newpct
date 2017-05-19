#!/usr/bin/env python
import os
import fnmatch
import sys
import re
import requests
from bs4 import BeautifulSoup


def getlistaseries(dirname):
    listaseries = os.listdir(dirname)
    listaseries.sort()
    return listaseries


def locate(pattern, root=os.curdir):
    '''Locate all files matching supplied filename pattern in and below
    supplied root directory.'''
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield filename


def menucapis(serieseleccionada, dirsrc):
    print "/-----------------------------------------------------------------\\"
    print "Serie seleccionada: %s" % serieseleccionada
    capis = []
    for avi in locate("*.avi", dirsrc + serieseleccionada):
        capis.append(avi[:-4])
    for mkv in locate("*.mkv", dirsrc + serieseleccionada):
        capis.append(mkv[:-4])
    if len(capis) > 0:
        capis.sort()
        if debug:
            print "Capitulos en disco:"
        for capi in capis:
            if debug:
                print "%s" % capi
            match = re.match(r'(.*)\[Cap.[0-9]{3,4}\](.*)', capi)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9'}
        payload = {'q': serieseleccionada}
        if debug:
            print "Buscando: %s" % serieseleccionada
        session = requests.Session()
        response = session.post('http://www.newpct.com/buscar-descargas/', headers=headers, data=payload)
        patron1 = match.group(1).replace('[', '\[').replace(']', '\]').replace('(','\(').replace(')','\)')
        patron2 = match.group(2).replace('[', '\[').replace(']', '\]')
        if debug:
            print "patron:%s<->%s" % (patron1, patron2)
            # print response.content
        soup = BeautifulSoup(response.content, "lxml")
        print "Capitulos disponibles:"
        for link in soup.find_all('a', href=True):
            if match.group(1) in link.text and match.group(2).decode('utf-8') in link.text:
                capiname = link.text.strip().encode('utf-8')
                matchmulticapi = re.match(r'(.*\[Cap.)([0-9]{3,4})_([0-9]{3,4})(\].*)', capiname)
                multifound = False
                if matchmulticapi:
                    multifound = True
                    print "MULTICAPI"
                    for i in range(int(matchmulticapi.group(2)), int(matchmulticapi.group(3))+1):
                        capinameextmulti = "%s%s%s" % (matchmulticapi.group(1), i, matchmulticapi.group(4))
                        print capinameextmulti
                        if capinameextmulti not in capis:
                            multifound = False
                print "%s" % capiname
                if (capiname not in capis) and multifound == False:
                    if not test:
                        print "Descargando: ->%s<-" % capiname
                    else:
                        print "Simulando: %s" % capiname
                    response2 = requests.get(link['href'])
                    soup2 = BeautifulSoup(response2.content, "lxml")
                    for link2 in soup2.find_all('a', href=True):
                        if ".torrent" in link2['href']:
                             if not test:
                                 os.system("ktorrent --silent %s" % link2['href'])
                             else:
                                 print link2['href']
    print "\-----------------------------------------------------------------/"
    return 'Salir'

os.environ['DISPLAY'] = ":0"
dirname = "/media/mazanas/Elements/Series/0_alive"
dirsrc = "/media/mazanas/Elements/Series/"
if len(sys.argv)>1 and sys.argv[1] == '1':
    debug = True
    print "Debug ON"
else:
    debug = False
if len(sys.argv)>1 and sys.argv[1] == 'test':
    test = True
    print "Test ON"
else:
    test = False
listaseries = getlistaseries(dirname)
for v in listaseries:
    selection = menucapis(v, dirsrc)
    while selection != 'Salir':
        selection = menucapis(v)