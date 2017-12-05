__author__ = 'leosamu'
import urllib2
from lxml.cssselect import CSSSelector
from lxml import html,etree
from urlparse import urljoin

validformats=['png','jpg','gif','bmp','tif']

def scrappWeb(url,filter,path,base):
    try:
        webdata =urllib2.urlopen(url)
    except:
        return url
    webstring = webdata.read()
    if filter == u'':
        return webstring
    #nyapa da morte for the android course.
    try:        
        htmlobj = html.fromstring(webstring.replace(u'font-size: 12px',u'font-size: 12pt'))
        sel = CSSSelector(filter)
        htmlobj = getImages(sel(htmlobj)[0],path,base)
        return html.tostring(sel(htmlobj)[0])
    except:
        return ""


def getImages(_htmlobj,path,_base):
    sel = CSSSelector("img")
    htmlobj=_htmlobj
    images = sel(htmlobj)
    for image in images:
        originalsrc = image.attrib["src"]
        if validImageFormat(originalsrc):
            if _base != "":
                fileUrl = getFileUrl(_base,originalsrc)
            else:
                fileUrl = getFileUrl(htmlobj.base,originalsrc)

            fileName = path + fileUrl.split('/')[-1].replace('%20','_')
            staticUrl = '/static/' + fileName.split('/')[-1]
            saveFile(fileUrl,fileName)
            image.attrib['src']=staticUrl
    return htmlobj

def saveFile(fileUrl,fileName):
    try:
        resource = urllib2.urlopen(fileUrl)
        output = open(fileName,"wb")
        output.write(resource.read())
        output.close()
    except:
        print "no se ha podido descargar" + fileUrl

def getFileUrl(url,src):
    if src.startswith('data:'):
        return src
    else:
        return urljoin(url,src).replace(' ','%20')


def validImageFormat(src):
    extension = src.split(".")[len( src.split("."))-1].lower()
    return extension in validformats
