def printMenu(req):
  output = """
  <div style='position:fixed;top:0;left:0;background-color:#ffffff;'>
  Args: %s 
  <a href='newpctseries.py'>SERIES</a>|
  <a href='newpctpelis.py'>PELIS</a>|
  <a href='newpctpelisimdb.py'>PELISIMDB</a>|
  <a href='newpctmkvimdb.py'>PELISIMDB MKV</a>|
  <a href='historico.py'>HISTORICO</a>|
  <a href='listarecientes.py'>RECIENTES</a>|
  <a href='newpctmicrohd.py'>MICROHD</a>|
  <a href='mp3.py'>MP3</a>|
  <a href='comics.py'>COMICS</a>
  </div><br/>
  """ % req.args
  return output
