__author__ = 'leosamu'
from PIL import Image
import urllib2
from StringIO import StringIO
from django.http import HttpResponse

def cropImg(url,left,top,right,bottom):
    imgdata = urllib2.urlopen(url)
    imgbin =imgdata.read()
    original = Image.open(StringIO(imgbin))
    croppedImage = original.crop((int(left), int(top), int(right), int(bottom)))

    response = HttpResponse(mimetype="image/png")
    croppedImage.save(response, "PNG")
    return response