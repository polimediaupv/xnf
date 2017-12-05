# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from conversor.XNF.models import Document
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from conversor.XNF.forms import DocumentForm
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from models import TranslateCourseStatus
from models import Alert
from XNFConversion import edx2xnf
from XNFConversion import xnf2edx
from XNFConversion import attachments
import datetime
from dateutil.tz import tzlocal
import imgcropper
import os, xlrd,json, time
import thread
import pymongo
from bson import json_util
import transchapterv2.edxOrgRest
import tarfile
import urllib2
import base64


def conversor(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES[u'input_excel']
            excel_data = input_excel.read()
            wb = xlrd.open_workbook(file_contents=excel_data)
            #try:
            generationresult = xnf2edx.generate_Edx(wb, "/tmp/importedfiles/" + request.user.username)

            #instead of this send to a report view that lets you download the file and shows the file resumé

            template = loader.get_template('XNF/report.html')
            context = RequestContext(request, {
                'coursename':generationresult["coursename"],
                'path': request.user.username +'/'+  generationresult["path"],
                'log': generationresult["log"],
                'error': generationresult["error"],
            })
            return HttpResponse(template.render(context))
            """
            filename = os.path.basename(generationresult["path"])
            response = HttpResponse(FileWrapper(open(generationresult["path"])),
                                   content_type='application/x-gzip')
            response['Content-Length'] = os.path.getsize(generationresult["path"])
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
            """
            #except Exception:
            #    print Exception
            #    form = DocumentForm()

    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    targz = []
    for root, dirs, files in os.walk('/tmp/importedfiles/'):
        for file in files:
            if file.endswith(".tar.gz"):
                created = time.ctime(os.path.getctime(root + '/' + file))
                lastmodified = time.ctime(os.path.getmtime(root + '/' + file))
                name = file.replace('.tar.gz','')
                user = root.replace('/tmp/importedfiles/','').replace('/'+name,'')
                targz.append({"created":created,"lastmodified":lastmodified,"name":name,"user":user})

    #path = '/tmp/importedfiles/leosamu'
    #targz = os.listdir(path)
    # Render list page with the documents and the form
    return render_to_response(
        'XNF/conversor.html',
        {'documents': documents, 'form': form, 'targz':targz},
        context_instance=RequestContext(request)
    )

def conversorM1(request):
    template = loader.get_template('XNF/conversorM1.html')
    context = RequestContext(request, {
        'coursename':"nombredelcurso",
        'path': "path al tar.gz",
        'log': "patatas",
        'error': "",
    })
    return HttpResponse(template.render(context))

def download(request):
    filename = "/tmp/importedfiles/redesdifraccionfibra/redesdifraccionfibra.tar.gz"
    response = HttpResponse(FileWrapper(open(generationresult["path"])),
                           content_type='application/x-gzip')
    response['Content-Length'] = os.path.getsize(generationresult["path"])
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def report(request):
    template = loader.get_template('XNF/report.html')
    context = RequestContext(request, {
        'coursename':"nombredelcurso",
        'path': "path al tar.gz",
        'log': "patatas",
        'error': "",
    })
    return HttpResponse(template.render(context))

def coursecalendar(request):
    template = loader.get_template('XNF/coursecalendar.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def coursesdates(request):
    srcconnection = pymongo.Connection("mongodb://edxdb1.cc.upv.es,edxdb2.cc.upv.es,edxdb3.cc.upv.es" , safe=True)
    srcdb = srcconnection.edxapp
    srcmodulestore = srcdb.modulestore
    findcourses = srcmodulestore.find({'_id.category': 'course'})
    courses = []
    for course in findcourses:
        end =''
        if 'end' in course['metadata'].keys():
            end = course['metadata']['end']
            courses.append({"title":course['metadata']['display_name'],"start":course['metadata']['start'],"end":end,"url":'http://upvx.es/courses/' + course['_id']['org'] + '/' + course['_id']['course'] + '/' + course['_id']['name'] + '/about'})
        else:
            if 'selfpaced' in request.GET and request.GET['selfpaced'] != 'false':
                end = datetime.datetime.now() + datetime.timedelta(days=365)
                courses.append({"title":course['metadata']['display_name'],"start":course['metadata']['start'],"end":end.isoformat(),"url":'http://upvx.es/courses/' + course['_id']['org'] + '/' + course['_id']['course'] + '/' + course['_id']['name'] + '/about',"selfpaced":'true'})

    response = HttpResponse(json.dumps(courses), content_type="application/json")
    #response["Access-Control-Allow-Origin"] = "*"
    return response

def transchapterv2view(request):
    courses = {} #mongocrud.getcourses(mongocrud.PAELLASERVERS)
    template = loader.get_template('XNF/transchapterv2.html')
    context = RequestContext(request, {
        'servers':transchapterv2.settings.SERVERS,
        'courses':courses
    })
    return HttpResponse(template.render(context))

def transchapterv2listcourse(request):
    #courses = transchapterv2.edxMongo.listActiveCourses()
    serverSource = (server for server in transchapterv2.settings.SERVERS if server["id"] == request.GET['serverid']).next()
    #login into the source server
    cookiesSource = transchapterv2.edxOrgRest.logIn(serverSource['url_lms'],serverSource['url_studio'],serverSource['user'],serverSource['password'])
    #get a list of courses in the source server
    coursesSource = transchapterv2.edxOrgRest.getCourses(serverSource['url_studio'],cookiesSource)
    return HttpResponse(json.dumps(coursesSource, sort_keys=True, indent=4, default=json_util.default))

def transchapterv2copychapter(request):
    '''
    :param request:
    :return:
    serverSource = (server for server in settings.SERVERS if server["name"] == "edxorg").next()
    serverTarget = (server for server in settings.SERVERS if server["name"] == "upvxtest").next()

    #login into the source server
    cookiesSource = logIn(serverSource['url_lms'],serverSource['url_studio'],serverSource['user'],serverSource['password'])
    #get a list of courses in the source server
    coursesSource = getCourses(serverSource['url_studio'],cookiesSource)
    #we chose the first course in the list as source course (for this example purpose)
    courseSource = getCourseStructure(serverSource['url_studio'],cookiesSource,coursesSource[0]['data-course-key'])
    #we chose the first chapter of the selected course to make a duplicate
    chapterSource = courseSource['child_info']['children'][0]

    #login into the target server
    cookiesTarget = logIn(serverTarget['url_lms'],serverTarget['url_studio'],serverTarget['user'],serverTarget['password'])
    #get a list of courses into the target server
    coursesTarget = getCourses(serverTarget['url_studio'],cookiesTarget)
    #for this example we will insert the chapter in the first course of the course list coursesTarget[0]['data-course-key']
    courseTarget = getCourseStructure(serverTarget['url_studio'],cookiesTarget,coursesTarget[0]['data-course-key'])

    #cross your fingers... (if u have defined correctly both servers u should have a copy of the first chapter of the first course of the serverSource
    #into the first course of the server target
    copyNode(serverSource['url_studio'],cookiesSource,serverTarget['url_studio'],cookiesTarget,courseTarget['id'],chapterSource)
    '''
    serverSource = (server for server in transchapterv2.settings.SERVERS if server["id"] == request.GET['serversrc']).next()
    cookiesSource = transchapterv2.edxOrgRest.logIn(serverSource['url_lms'],serverSource['url_studio'],serverSource['user'],serverSource['password'])
    serverTarget = (server for server in transchapterv2.settings.SERVERS if server["id"] == request.GET['serverdst']).next()
    if serverSource == serverTarget:
        cookiesTarget = cookiesSource
    else:
        cookiesTarget = transchapterv2.edxOrgRest.logIn(serverTarget['url_lms'],serverTarget['url_studio'],serverTarget['user'],serverTarget['password'])
    courseSource = transchapterv2.edxOrgRest.getCourseStructure(serverSource['url_studio'],cookiesSource,request.GET['coursesrc'])
    #we chose the first chapter of the selected course to make a duplicate
    chapterSource = (chapter for chapter in courseSource['child_info']['children'] if chapter["id"] == request.GET['chaptersrc']).next()
    transchapterv2.edxOrgRest.copyNode(serverSource['url_studio'],cookiesSource,serverTarget['url_studio'],cookiesTarget,request.GET['coursedst'].replace('course-v1','block-v1') + '+type@course+block@course',chapterSource)

    #courses = transchapterv2.edxMongo.copyChapter(request.GET['serversrc'],request.GET['coursesrc'],request.GET['chaptersrc'],request.GET['serverdst'],request.GET['coursedst'])
    return HttpResponse(True)

def transchapterv2listchapters(request):
    #courses = transchapterv2.edxMongo.listActiveCourses()
    serverSource = (server for server in transchapterv2.settings.SERVERS if server["id"] == request.GET['serverid']).next()
    #login into the source server
    cookiesSource = transchapterv2.edxOrgRest.logIn(serverSource['url_lms'],serverSource['url_studio'],serverSource['user'],serverSource['password'])
    #get a list of courses in the source server
    course = transchapterv2.edxOrgRest.getCourseStructure(serverSource['url_studio'],cookiesSource,request.GET['courseid'])
    #course = transchapterv2.edxMongo.getCourseStructure(request.GET['serverid'],request.GET['courseid'])
    chapters = []
    for block in course['child_info']['children']:
        if block['category']=='chapter':
            chapters.append(block)
    return HttpResponse(json.dumps(chapters, sort_keys=True, indent=4, default=json_util.default))

def attachsubs(request):
    courses = mongocrud.getcourses(mongocrud.PAELLASERVERS)
    template = loader.get_template('XNF/attachsubs.html')
    context = RequestContext(request, {
        'servers':mongocrud.PAELLASERVERS,
        'courses':courses
    })
    return HttpResponse(template.render(context))


def ytapi(request):
    template = loader.get_template('XNF/ytapi.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def ytmsg(request):
    template = loader.get_template('XNF/youtubemsg.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def edxorgactivity(request):
    template = loader.get_template('XNF/edxorgactivity.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def newuser(request):
    template = loader.get_template('XNF/createnewuser.html')
    context = RequestContext(request, {

    })
    return HttpResponse(template.render(context))

def createnewuser(request):
    #update the profile
    u = User.objects.create_user(request.REQUEST['user'],request.REQUEST['mail'],request.REQUEST['pass'])
    u.save()
    return HttpResponse('gogo')


def updateprofile(request):
    #update the profile
    u = User.objects.get(username=request.user.username)
    u.email=request.REQUEST['mail']
    u.username=request.REQUEST['user']
    if request.REQUEST['pass']!=u'keep the same':
        u.set_password(request.REQUEST['pass'])
    u.save()
    return HttpResponse('gogo')

def profile(request):
    template = loader.get_template('XNF/profile.html')
    context = RequestContext(request, {

    })
    return HttpResponse(template.render(context))

def index(request):
    template = loader.get_template('XNF/index.html')
    context = RequestContext(request, {

    })
    return HttpResponse(template.render(context))

def copychapter(request):
    context = RequestContext(request)
    text = None
    if request.method == 'GET':
        chapterName = request.GET['chapter_name']
        srvOrigen = request.GET['srvOrigen']
        courseOrigen = request.GET['courseOrigen']
        srvDestination = request.GET['srvDestination']
        courseDestination = request.GET['courseDestination']
        text = trans_chapter.copy_chapter(srvOrigen,courseOrigen,chapterName,srvDestination,courseDestination)
    return HttpResponse(text)

def addsubs(request):
    context = RequestContext(request)
    text = None
    if request.method == 'GET':
        chapterName = request.GET['chapter_name']
        srvOrigen = request.GET['srvOrigen']
        courseOrigen = request.GET['courseOrigen']
        language = json.loads(request.GET['language'])
        text = trans_subs.get_subs(srvOrigen,courseOrigen,chapterName,language,unicode(request.user))
        text = "roger"
    return HttpResponse(text)

def youtubesub(request):
    xml = {}
    if request.method == 'GET':
        if "videoID" in request.GET.keys() and 'lang_code' in request.GET.keys():
            videoID = request.GET['videoID']
            lang_code = request.GET['lang_code']
            xml = ytapicrud.getsubsxml(videoID,lang_code)
        else:
            xml= "no videoID no data :P"
    response = HttpResponse(xml, content_type="application/xml")
    response["Access-Control-Allow-Origin"] = "*"
    return response

def imgcrop(request):
    context = RequestContext(request)
    if request.method == 'GET':
        url = request.GET['url']
        top = request.GET['top']
        left = request.GET['left']
        right = request.GET['right']
        bottom = request.GET['bottom']

        imgcropped =  imgcropper.cropImg(url,left,top,right,bottom)
    return imgcropped



def edxorggetcourses(request):
    context = RequestContext(request)
    json = None
    if request.method == 'GET':

        json =  edxorgcrud.getcourses()

    return HttpResponse(json, content_type="application/json") #HttpResponse(json)

def startEdx2Xnf(request):
    assert request.method=="POST"
    print "receive.META.SERVER_PORT", request.META["SERVER_PORT"], request.POST
    filename = "/tmp/edx2xnf/" + request.user.username + "/" + request.FILES['file'].name
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    fd = open(filename,'a+')
    for chunk in request.FILES['file'].chunks():
        fd.write(chunk)
    #here we need to send the converion request
    #translatetool.translatecourses.translate(request.POST["srcLang"],request.POST["trgLang"],filename,request.user.username)
    return HttpResponse("me-%s-RECEIVE-OK[POST=%s,files=%s]" % (request.META["SERVER_PORT"], request.POST.values(), "ok" ))


def startTranslate(request):
    assert request.method=="POST"
    print "receive.META.SERVER_PORT", request.META["SERVER_PORT"], request.POST
    filename = "/tmp/translationcourses/" + request.user.username + "/" + request.FILES['file'].name
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    fd = open(filename,'a+')
    for chunk in request.FILES['file'].chunks():
        fd.write(chunk)
    translatetool.translatecourses.translate(request.POST["srcLang"],request.POST["trgLang"],filename,request.user.username)
    return HttpResponse("me-%s-RECEIVE-OK[POST=%s,files=%s]" % (request.META["SERVER_PORT"], request.POST.values(), "ok" ))

def addCSVconversion(request):
    assert request.method=="POST"
    print "receive.META.SERVER_PORT", request.META["SERVER_PORT"], request.POST
    filename = request.POST["coursepath"] + request.FILES['file'].name
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    fd = open(filename,'a+')
    for chunk in request.FILES['file'].chunks():
        fd.write(chunk)
    attachments.addCSV(request.POST["coursepath"],filename)
    #translatetool.translatecourses.translate(request.POST["srcLang"],request.POST["trgLang"],filename,request.user.username)
    return HttpResponse("me-%s-RECEIVE-OK[POST=%s,files=%s]" % (request.META["SERVER_PORT"], request.POST.values(), "ok" ))

def addPoliciesconversion(request):
    assert request.method=="POST"
    print "receive.META.SERVER_PORT", request.META["SERVER_PORT"], request.POST
    filename = '/tmp/policies/' + request.FILES['file'].name
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    fd = open(filename,'a+')
    for chunk in request.FILES['file'].chunks():
        fd.write(chunk)
    attachments.addPolicies(request.POST["coursepath"],filename)
    #translatetool.translatecourses.translate(request.POST["srcLang"],request.POST["trgLang"],filename,request.user.username)
    return HttpResponse("me-%s-RECEIVE-OK[POST=%s,files=%s]" % (request.META["SERVER_PORT"], request.POST.values(), "ok" ))

def getCourseTranslation(request):
    json = {}
    if request.method == 'GET':
        if "courseId" in request.GET.keys():
            courseId = request.GET['courseId']
            sourcedir = "/tmp/translationcourses/" + request.user.username + "/" + courseId
            filepath = sourcedir + ".tar.gz"
            with tarfile.open(filepath,"w:gz") as tar:
                tar.add(sourcedir,arcname=os.path.basename(sourcedir))
            filename = "/tmp/importedfiles/redesdifraccionfibra/redesdifraccionfibra.tar.gz"
            response = HttpResponse(FileWrapper(open(filepath)),
                                   content_type='application/x-gzip')
            response['Content-Length'] = os.path.getsize(filepath)
            response['Content-Disposition'] = "attachment; filename=%s" % courseId + ".tar.gz"
            return response
        else:
            return HttpResponse("me-%s-Course-not-found[POST=%s,files=%s]" % (request.META["SERVER_PORT"], request.POST.values(), "ok" ))







