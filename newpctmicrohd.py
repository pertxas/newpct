import mechanize
import newpctmenu

def index(req):

  br = mechanize.Browser()
  br.set_handle_robots(False)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; es-VE; rv:1.9.0.1)Gecko/2008071615 Debian/6.0 Firefox/9')]
  r = br.open('http://www.newpct.com/cine-alta-definicion-hd/')
  output = "<html><head></head><body>"
  output += newpctmenu.printMenu(req)
  output += "<h1>MICROHD</h1>"
  for line in r.readlines():
    if 'imgBank/d' in line and 'MicroHD' in line:
      output += line.replace("alt=", "title=")
  output += '</body></html>'
  return output
