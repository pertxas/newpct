import mechanize
import re
from bs4 import BeautifulSoup
import psycopg2
import traceback
import newpctmenu


def parseimdb(newurl):
    urlbase = 'http://www.imdb.com'
    url = newurl.replace(urlbase, '')
    br2 = mechanize.Browser()
    r2 = br2.open('%s%s' % ('' if newurl.startswith('http') else urlbase, newurl))
    soup2 = BeautifulSoup(r2.read(), 'html.parser')
    div = soup2.find('div', {'class': 'heroic-overview'})
    if not div:
        return "NOT FOUND"
    subtext = div.find('div', {'class': 'subtext'})
    if not subtext:
        subtext = ''
    else:
        subtext = subtext.get_text().encode('utf-8')
    rating = div.find('div', {'class': 'ratingValue'})
    if not rating:
        rating = ''
    else:
        rating = rating.get_text().encode('utf-8')
    poster = div.find('div', {'class': 'poster'})
    if not poster:
        poster = ''
    else:
        poster = poster.prettify('utf-8').replace('href="/', 'target="_blank" href="%s/' % urlbase)
    slate = div.find('div', {'class': 'slate'})
    if not slate:
        slate = ''
    else:
        slate = slate.prettify('utf-8').replace('href="/', 'target="_blank" href="%s/' % urlbase)
    plot = soup2.find('div', {'class': 'plot_summary'})
    linedata = "<table>"
    linedata += "<tr>"
    linedata += "<td style=\"width:182px;\">%s</td>" % poster
    linedata += "<td>%s</td>" % slate
    linedata += "</tr>"
    linedata += "<tr><td colspan = \"2\">%s | %s </td></tr>" % (subtext, rating)
    linedata += "<tr><td colspan = \"2\">%s</td></tr>" % plot.prettify('utf-8')
    linedata += "<tr><td colspan = \"2\">URL: <a href=\"%s%s\" target=\"_blank\">%s</a></td></tr>" % (
        urlbase, url.encode('utf-8'), url.encode('utf-8'))
    linedata += "</table>"
    return linedata


def getsoupimdb(title):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9')]
    br.open('http://imdb.com')
    br.select_form(nr=0)
    br.form['q'] = '%s' % title.encode('utf-8')
    br.submit()
    r = br.response()
    soup = BeautifulSoup(r.read(), 'html.parser')
    return soup


def getsoupfilm(title):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent',
                      'Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9')]
    br.open('http://filmaffinity.com')
    br.select_form(nr=0)
    br.form['stext'] = '%s' % title.encode('utf-8')
    br.submit()
    r = br.response()
    soup = BeautifulSoup(r.read(), 'html.parser')
    return soup


def scrapimdb(filename):
    output = ""
    linedata = ""
    match_obj = re.match(r'(.+?(?= \[| \())', filename)
    if match_obj:
        try:
            title = match_obj.group(1)
            title = title.replace(' V Extendida', '')
        except Exception as e:
            output += "<span class=\"error\">%s, %s</span><br/>" % (e, traceback.format_exc())
    else:
        output += "<span class=\"error\">ERROR REGEX</span><br/>"
        title = filename.replace(' Castellano BDrip 720p X264', '')
    soup = getsoupimdb(title)
    table = soup.find('table', {'class': 'findList'})
    if table:
        links = table.find_all('a')
        url = links[0]['href']
        linedata = parseimdb(url)
    else:
        soup = getsoupfilm(title)
        output += soup.prettify('utf-8')
        linedata = "NOT FOUND"
        url = ""
    conn = psycopg2.connect('dbname=imdb user=imdb host=localhost password=imdb')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO recientes (file,data,url) VALUES (%s,%s,%s);", (filename, linedata, url))
    conn.commit()
    cursor.close()

    output += linedata
    return output


def index(req):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9')]
    r = br.open('http://www.newpct.com/peliculas-x264-mkv/')
    output = "<html><head>"
    output += "<meta charset=\"utf-8\">"
    output += "<style>"
    output += ".error {color: red;}"
    output += ".inline {display: inline;}"
    output += "table {border: 1px solid black;table-layout: fixed;width: 670px;}"
    output += "</style>"
    output += "</head><body>"
    output += newpctmenu.printMenu(req)
    output += "<h1>PELISIMDB MKV</h1>"
    outputlinks = "<html><head></head><body>"
    for line in r.readlines():
        if 'imgBank/d' in line and "Descargar Peliculas x264" in line and "creener" not in line:
            outputlinks += line.replace("alt=", "title=").decode('windows-1252').encode('utf-8')

    soup = BeautifulSoup(outputlinks + "</body></html>", 'html.parser')
    output += "<br/>"
    imgs = soup.find_all('img')
    conn = psycopg2.connect('dbname=imdb user=imdb host=localhost password=imdb')
    for img in imgs:
        filename = img['title'][29:].replace('_', ' ')
        output += "<h1>%s%s</h1>" % (img.prettify('utf-8'), filename.encode('utf-8'))
        cursor = conn.cursor()
        cursor.execute("SELECT file, data, url from recientes where file='%s';" % filename)
        linedata = ""
        if cursor.rowcount > 0:
            linedata += cursor.fetchone()[1]
        else:
            # pass
            linedata += scrapimdb(filename)
        output += linedata
    cursor.close()
    conn.close()
    output += "</body></html>"
    return output
