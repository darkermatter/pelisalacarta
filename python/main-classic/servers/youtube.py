# s-*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Youtube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import cgi
import re
import urllib

from core import logger
from core import scrapertools

from core import jsontools as json

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[youtube.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    #page_url = "http://www.youtube.com/get_video_info?&video_id=zlZgGlwBgro"
    if not page_url.startswith("http"):
        page_url = "http://www.youtube.com/watch?v=%s" % page_url
        logger.info("[youtube.py] page_url->'%s'" % page_url)
        
    # Lee la p�gina del video
    data = scrapertools.cache_page( page_url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']] , )
    '''
    data = scrapertools.get_match(data,"yt.playerConfig \= (.*?)yt.setConfig")
    data = data.replace("\\","")
    logger.info("-------------------------------------------------------------------------------------------")
    logger.info("data="+data)
    logger.info("-------------------------------------------------------------------------------------------")

    # "fmt_list": "37/1920x1080/9/0/115,22/1280x720/9/0/115,84/1280x720/9/0/115,35/854x480/9/0/115,34/640x360/9/0/115,18/640x360/9/0/115,82/640x360/9/0/115,5/320x240/7/0/0,36/320x240/99/0/0,17/176x144/99/0/0"
    fmt_list = urllib.unquote( scrapertools.get_match(data,'"fmt_list"\: "([^"]+)"') )
    logger.info(fmt_list)
    fmt_list_array = fmt_list.split(",")

    # "url_encoded_fmt_stream_map": 
    #    "fallback_host=tc.v15.cache6.c.youtube.com\u0026sig=6CB93CBC67CF3B593A6C5193A40246D43879EC12.3EC65E221B0113A8EAA63F0A059F91A24C0ABEF9\u0026itag=37\u0026url=http%3A%2F%2Fr6---sn-h5q7enel.c.youtube.com%2Fvideoplayback%3Fkey%3Dyt1%26ip%3D80.26.225.23%26sver%3D3%26expire%3D1358232284%26itag%3D37%26fexp%3D920704%252C912806%252C922403%252C922405%252C929901%252C913605%252C925710%252C929104%252C929110%252C908493%252C920201%252C913302%252C919009%252C911116%252C910221%252C901451%26source%3Dyoutube%26mv%3Dm%26newshard%3Dyes%26ms%3Dau%26upn%3DKJ4LhwFLl7g%26ratebypass%3Dyes%26id%3D9cbfb0c3e5c7b5a6%26mt%3D1358208854%26sparams%3Dcp%252Cgcr%252Cid%252Cip%252Cipbits%252Citag%252Cratebypass%252Csource%252Cupn%252Cexpire%26gcr%3Des%26ipbits%3D8%26cp%3DU0hUTVJOUF9NTkNONF9KSFRDOkJnNE9EUGNUeWtj\u0026quality=hd1080\u0026type=video%2Fmp4%3B+codecs%3D%22avc1.64001F%2C+mp4a.40.2%22
    #     ,fallback_host=
    fmt_stream_map = urllib.unquote( scrapertools.get_match(data,'"url_encoded_fmt_stream_map"\: "([^"]+)"') )
    logger.info(fmt_stream_map)
    fmt_stream_map_array = fmt_stream_map.split(",")

    logger.info("-------------------------------------------------------------------------------------------")
    logger.info("len(fmt_list_array)=%d" % len(fmt_list_array))
    logger.info("len(fmt_stream_map_array)=%d" % len(fmt_stream_map_array))

    CALIDADES = {'5':'240p','34':'360p','18':'360p','35':'480p','22':'720p','84':'720p','37':'1080p','38':'3072p','17':'144p','43':'360p','44':'480p','45':'720p'}

    for i in range(len(fmt_list_array)):
        try:
            video_url = urllib.unquote(fmt_stream_map_array[i])
            logger.info("video_url="+video_url)
            video_url = urllib.unquote(video_url[4:])
            video_url = video_url.split(";")[0]
            logger.info(" [%s] - %s" % (fmt_list_array[i],video_url))
            
            calidad = fmt_list_array[i].split("/")[0]
            video_url = video_url.replace("flv&itag="+calidad,"flv")
            video_url = video_url.replace("="+calidad+"&url=","")
            video_url = video_url.replace("sig=","signature=")
            video_url = re.sub("^=http","http",video_url)

            resolucion = fmt_list_array[i].split("/")[1]
    
            formato = ""
            patron = '&type\=video/([a-z0-9\-]+)'
            matches = re.compile(patron,re.DOTALL).findall(video_url)
            if len(matches)>0:
                formato = matches[0]
                if formato.startswith("x-"):
                    formato = formato[2:]
                formato = formato.upper()
    
            etiqueta = ""
            try:
                etiqueta = CALIDADES[calidad]
                if formato!="":
                    etiqueta = etiqueta + " (%s a %s) [youtube]" % (formato,resolucion)
                else:
                    etiqueta = etiqueta + " (%s) [youtube]" % (resolucion)
        
                video_urls.append( [ etiqueta , video_url ])
            except:
                pass
            
        except:
            pass
    '''
    video_urls = scrapeWebPageForVideoLinks(data)

    video_urls.reverse()
    
    for video_url in video_urls:
        logger.info(str(video_url))
    
    return video_urls
'''
def extractFlashVars(data):
    flashvars = {}
    #found = False
    patron = '<script>.*?ytplayer.config = (.*?);</script>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if matches:
        data = json.loads(matches[0])
        flashvars = data["args"]
    #logger.info("flashvars: " + repr(flashvars))
    return flashvars
'''
def removeAdditionalEndingDelimiter(data):                            
        pos = data.find("};")                                          
        if pos != -1:                                                  
             logger.info(u"found extra delimiter, removing")         
             data = data[:pos + 1]                                       
        return data                                                  
                                                               
def normalizeUrl(self, url):                               
        if url[0:2] == "//":                                       
            url = "http:" + url                                   
        return url 
def extractFlashVars(data):
	assets=0
        flashvars = {}                                                  
        found = False                                                   
                                                                     
        for line in data.split("\n"):                                                 
            if line.strip().find(";ytplayer.config = ") > 0:                          
                found = True                                                          
                p1 = line.find(";ytplayer.config = ") + len(";ytplayer.config = ") - 1
                p2 = line.rfind(";")                                                  
                if p1 <= 0 or p2 <= 0:                                                
                    continue                                                          
                data = line[p1 + 1:p2]                                                
                break                                                                 
        data = removeAdditionalEndingDelimiter(data)                             
                                                                                      
        if found:                                                                     
            data = json.load_json(data)
            if assets:                                                                
                flashvars = data["assets"]                                            
            else:                                                                     
                flashvars = data["args"]                                              
                                                                                      
        for k in ["html", "css", "js"]:                                               
            if k in flashvars:                                                        
                flashvars[k] = normalizeUrl(flashvars[k])
                                                              
        logger.info("Step2: " + repr(data))            
                                                              
        logger.info(u"flashvars: " + repr(flashvars))  
        return flashvars

def scrapeWebPageForVideoLinks(data):
    logger.info("")
    links = {}

    fmt_value = {
        5: "240p h263 flv",
        6: "240p h263 flv",
        18: "360p h264 mp4",
        22: "720p h264 mp4",
        26: "???",
        33: "???",
        34: "360p h264 flv",
        35: "480p h264 flv",
        36: "3gpp",
        37: "1080p h264 mp4",
        38: "4K h264 mp4",
        43: "360p vp8 webm",
        44: "480p vp8 webm",
        45: "720p vp8 webm",
        46: "1080p vp8 webm",
        59: "480p h264 mp4",
        78: "480p h264 mp4",
        82: "360p h264 3D",
        83: "480p h264 3D",
        84: "720p h264 3D",
        85: "1080p h264 3D",
        100: "360p vp8 3D",
        101: "480p vp8 3D",
        102: "720p vp8 3D",
        133: "240p h264 mp4",
        134: "360p h264 mp4",
        135: "480p h264 mp4",
        136: "720p h264 mp4",
        137: "1080p h264 mp4",
        264: "1440p h264 mp4",
        266: "4K h264 mp4",
        298: "720p mp4 60fps",
        299: "1080p mp4 60fps",
        218: "480p vp9 webm",
        219: "480 vp9 webm",
        242: "240p vp9 webm",
        243: "360p vp9 webm",
        244: "480p vp9 webm",
        245: "480p vp9 webm",
        246: "480p vp9 webm",
        247: "720p vp9 webm",
        248: "1080p vp9 webm",
        271: "1440p vp9 webm",
        272: "4K webm 60fps",
        302: "720p webm 60fps",
        303: "1080p webm 60fps",
        308: "1440p webm 60fps",
        313: "4K vp9 webm",
        315: "4K webm 60fps"
        }
    exclude_itags = [17, 139, 140, 141, 160, 171, 172, 249, 250, 251, 256, 258, 278]

    video_urls=[]

    flashvars = extractFlashVars(data)
    if not flashvars.has_key(u"url_encoded_fmt_stream_map"):
        return links

    if flashvars.has_key(u"ttsurl"):
        logger.info("ttsurl="+flashvars[u"ttsurl"])

    if flashvars.has_key('hlsvp'):
        url = flashvars[u"hlsvp"]
        video_urls.append( [ "(LIVE .m3u8) [youtube]" , url ])
        return video_urls
    
    js_signature = ""
    try:
        data_flashvars = flashvars[u"adaptive_fmts"].split(u",")
    except:
        data_flashvars = flashvars[u"url_encoded_fmt_stream_map"].split(u",")

    for url_desc in data_flashvars:
        url_desc_map = cgi.parse_qs(url_desc)
        logger.info(u"url_map: " + repr(url_desc_map))
        if not (url_desc_map.has_key(u"url") or url_desc_map.has_key(u"stream")):
            continue

        try:
            key = int(url_desc_map[u"itag"][0])
            if key in exclude_itags:
                continue
            url = u""
            if url_desc_map.has_key(u"url"):
                url = urllib.unquote(url_desc_map[u"url"][0])
            elif url_desc_map.has_key(u"conn") and url_desc_map.has_key(u"stream"):
                url = urllib.unquote(url_desc_map[u"conn"][0])
                if url.rfind("/") < len(url) -1:
                    url = url + "/"
                url = url + urllib.unquote(url_desc_map[u"stream"][0])
            elif url_desc_map.has_key(u"stream") and not url_desc_map.has_key(u"conn"):
                url = urllib.unquote(url_desc_map[u"stream"][0])

            if url_desc_map.has_key(u"sig"):
                url = url + u"&signature=" + url_desc_map[u"sig"][0]
            elif url_desc_map.has_key(u"s"):
                sig = url_desc_map[u"s"][0]
                if not js_signature:
                    urljs = scrapertools.find_single_match(data, '"assets":.*?"js":\s*"([^"]+)"')
                    urljs = urljs.replace("\\", "")
                    if urljs:
                        data_js = scrapertools.downloadpage("http:"+urljs)
                        from jsinterpreter import JSInterpreter
                        funcname = scrapertools.find_single_match(data_js, '\.sig\|\|([A-z0-9$]+)\(')

                        jsi = JSInterpreter(data_js)
                        js_signature = jsi.extract_function(funcname)

                signature = js_signature([sig])
                url += u"&signature=" + signature

            # Se encodean las comas para que no falle en método built-in
            url = url.replace(",", "%2C")
            video_urls.append( [ "("+fmt_value[key]+") [youtube]" , url ])
        except:
            import traceback
            logger.info(traceback.format_exc())

    return video_urls

def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = 'youtube(?:-nocookie)?\.com/(?:(?:(?:v/|embed/))|(?:(?:watch(?:_popup)?(?:\.php)?)?(?:\?|#!?)(?:.+&)?v=))?([0-9A-Za-z_-]{11})'#'"http://www.youtube.com/v/([^"]+)"'
    logger.info("[youtube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = "http://www.youtube.com/watch?v="+match
        
        if url!='':
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'youtube' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)
    
    patronvideos  = 'www.youtube.*?v(?:=|%3D)([0-9A-Za-z_-]{11})'
    logger.info("[youtube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = "http://www.youtube.com/watch?v="+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'youtube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.youtube.com/v/AcbsMOMg2fQ
    patronvideos  = 'youtube.com/v/([0-9A-Za-z_-]{11})'
    logger.info("[youtube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[YouTube]"
        url = "http://www.youtube.com/watch?v="+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'youtube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
