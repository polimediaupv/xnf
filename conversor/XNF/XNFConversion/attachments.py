__author__ = 'leosamu'

import csv
import os, tarfile
from lxml import etree,html
import json
import StringIO


def addCSV(coursepath,csvname):
    #we check the video folder on course path.
    for file in os.listdir(coursepath + 'video'):
        if file.endswith(".xml"):
            tree = etree.parse(coursepath + 'video/' + file)
            youtubeID = tree.getroot().attrib['youtube_id_1_0']
            #for evry video we find it in the csv
            with open(csvname, 'rb') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in csvreader:
                    try:
                        if row[8] == youtubeID:
                        #we attach the video info from the csv to the xml
                            root = tree.getroot()
                            root.attrib['license']="creative-commons: ver=4.0 BY NC ND"
                            root.attrib['download_video']="true"
                            root.attrib['edx_video_id']=row[3]
                            root.attrib['only_on_web']="false"
                            video_asset = etree.SubElement(root, 'video_asset', client_video_id=row[0],duration="0")
                            desktopH = etree.SubElement(video_asset,'encoded_video', bitrate="348", file_size="", profile="desktop_mp4", url=row[5])
                            mobileL = etree.SubElement(video_asset,'encoded_video', bitrate="173", file_size="", profile="mobile_low", url=row[7])
                            youtube = etree.SubElement(video_asset,'encoded_video', bitrate="0", file_size="0", profile="youtube", url=youtubeID)
                            tree.write(coursepath + 'video/' + file, pretty_print=True, xml_declaration=False, encoding='utf-8')
                    except:
                        print "uh?"
    #we genrate again the tarball

    os.remove(coursepath + coursepath.split('/')[len(coursepath.split('/'))-2] + '.tar.gz')
    make_tarfile(coursepath)
    #job done
    pass

def addPolicies(coursepath,tarballname):
    pre=''
    #we check if its a tarball...
    if tarballname[-6:]!='tar.gz':
        return -1
    #we open the tarball
    tar = tarfile.open(tarballname, 'r')
    #parent folder structure control may need to change in future if they change this again
    if 'course.xml' not in tar.getnames():
        pre = 'course/'
    #get origin course files
    coursefilename = pre + 'course.xml'
    course = etree.parse(StringIO.StringIO(tar.extractfile(tar.getmember(coursefilename)).read()),etree.XMLParser(recover=True,encoding='utf-8')).getroot()
    coursedescriptionfilename = pre + 'course/' + course.attrib['url_name'] + '.xml'
    coursedescription = etree.parse(StringIO.StringIO(tar.extractfile(tar.getmember(coursedescriptionfilename)).read()),
                         etree.XMLParser(recover=True, encoding='utf-8')).getroot()
    #get target course files
    coursetargetfilename = coursepath + 'course.xml'
    coursetarget = etree.parse(StringIO.StringIO(open(coursetargetfilename,'r').read()),
                               etree.XMLParser(recover=True,encoding='utf-8')).getroot()
    coursetargetdescriptionfilename = coursepath + 'course/' + coursetarget.attrib['url_name'] + '.xml'
    coursetargetdescription = etree.parse(StringIO.StringIO(open(coursetargetdescriptionfilename).read()),
                               etree.XMLParser(recover=True, encoding='utf-8')).getroot()
    #combine origin into target
    for att in coursedescription.attrib:
        if att not in coursetargetdescription.attrib:
            coursetargetdescription.attrib[att] = coursedescription.attrib[att]
    doc = etree.ElementTree(coursetargetdescription)

    doc.write(coursetargetdescriptionfilename, pretty_print=True, xml_declaration=False, encoding='utf-8')


    #check policies file
    policiefilename = pre + 'policies/' + course.attrib['url_name'] + '/policy.json'
    policiesfile = tar.extractfile(tar.getmember(policiefilename)).read()
    policies = json.loads(policiesfile)
    #get policies target file
    policiestargetfilename = coursepath + 'policies/' + coursetarget.attrib['url_name'] + '/policy.json'
    policiestarget = json.load(open(policiestargetfilename,'r'))
    #combine origin into target
    for att in policies['course/' + course.attrib['url_name']]:
        if att not in policiestarget['course/' + coursetarget.attrib['url_name']]:
            policiestarget['course/' + coursetarget.attrib['url_name']][att] = policies['course/' + course.attrib['url_name']][att]
    #policiestarget['course/' + coursetarget.attrib['url_name']]
    with open(policiestargetfilename, 'wb') as fp:
        json.dump(policiestarget, fp)

    #check static files
    staticfiles = [tarinfo for tarinfo in tar.getmembers() if tarinfo.name.startswith('course/static')]
    for file in staticfiles:
        file.path=file.path.replace(pre,'')
    tar.extractall(coursepath,members=staticfiles)



    #generate tarball again
    os.remove(coursepath + coursepath.split('/')[len(coursepath.split('/')) - 2] + '.tar.gz')
    make_tarfile(coursepath)
    #job done
    pass

def make_tarfile(path):
    """
    Packs all in a targz file ready to import.
    """
    try:
        tarpath = path + path.split('/')[len(path.split('/'))-2] + '.tar.gz'
        with tarfile.open( tarpath , 'w:gz') as tar:
            for f in os.listdir(path):
                tar.add(path + "/" + f, arcname=os.path.basename(f))
            tar.close()
    except Exception, e:
        print e