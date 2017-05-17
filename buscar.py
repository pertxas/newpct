#!/usr/bin/env python

import requests
import sys
import os
from bs4 import BeautifulSoup

os.environ['DISPLAY'] = ":0"

if len(sys.argv) > 1:
    busqueda = sys.argv[1]
else:
    busqueda = raw_input("buscar: ")

headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9'}
payload = {'q': busqueda}

session = requests.Session()
response = session.post('http://www.newpct.com/buscar-descargas/', headers=headers, data=payload)
cs = ''
while cs != 'Salir':
    enlaces = []
    enlacestext = []
    enlaces.append('')
    enlacestext.append('Salir')
    print "[%i] %s" % (0, 'Salir')
    n = 1
    soup = BeautifulSoup(response.content, "lxml")
    for link in soup.find_all('a', href=True):
        #print link
        try:
            title = link.attrs['title']
        except:
            title = ''
        if "sobre" in title:
            # print link
            enlaces.append(link['href'])
            enlacestext.append(link.text)
            print "[%i] %s" % (n, link.text)
            n = n + 1
    # print enlaces
    select = int(raw_input("elige: "))
    capiseleccionado = enlaces[select]
    capiseleccionadotext = enlacestext[select]
    if capiseleccionadotext != 'Salir':
        response = requests.get(capiseleccionado)
        soup = BeautifulSoup(response.content, "lxml")
        for link in soup.find_all('a', href=True):
            if ".torrent" in link['href']:
                print link['href']
                os.system("ktorrent --silent %s" % link['href'])
                cs= 'Salir'
