#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib,urllib2, cookielib,json
import sys
import settings
import pdb
from lxml.cssselect import CSSSelector
from lxml import html

reload(sys)
sys.setdefaultencoding('utf8')



def logIn(_lms_server,_cms_server,_user,_password):
    '''
    log in into the lms server and return the required cookies to use the
    studio internal api
    '''
    cj = cookielib.CookieJar()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)


    response = opener.open(_lms_server +'/login')
    set_cookie = {}
    for cookie in cj:
        set_cookie[cookie.name] = cookie.value
    #Prepare Headers
    headers = {'User-Agent': 'edX-downloader/0.01',
               'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
               'Referer': _lms_server,
               'X-Requested-With': 'XMLHttpRequest',
               'X-CSRFToken': set_cookie.get('csrftoken', '') }

    #Login
    post_data = urllib.urlencode({
                'email' : _user,
                'password' : _password,
                'remember' : False
                }).encode('utf-8')
    request = urllib2.Request(_lms_server + '/user_api/v1/account/login_session/', post_data,headers)
    response = urllib2.urlopen(request)

    response = opener.open(_cms_server)
    for cookie in cj:
        set_cookie[cookie.name] = cookie.value
    return set_cookie

def getCourses(_cms_server,_set_cookie):
    '''
    connect to studio server and get a list of the courses where the logged user is admin/instructor
    '''
    url = _cms_server +'/home/'
    cookies = ""
    for key, value in _set_cookie.iteritems():
        cookies = cookies + key + ' = ' + value + ';'
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        'X-CSRFToken': _set_cookie.get('csrftoken', ''),
        'content-type': "application/json; charset=UTF-8",
        'accept-encoding': "gzip, deflate",
        'Referer': 'https://studio.edx.org/',
        'accept-language': "es,en;q=0.8,en-US;q=0.6",
        'cookie': cookies,
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers)
    result = response.text
    array_course_listing = json.loads(result[result.index('new StudioCourseIndex(\n        ".react-course-listing",\n        ')+len('new StudioCourseIndex(\n        ".react-course-listing",\n        '):result.index(',\n        enableReruns\n    );')])
    result2=result[result.index('new StudioArchivedIndex(\n        ".react-archived-course-listing",\n        ')+len('new StudioArchivedIndex(\n        ".react-archived-course-listing",\n        '):]
    array_archive_listing = json.loads(result2[:result2.index(',\n        enableReruns\n    );')])
    courses = []
    for i in range(len(array_course_listing)):
        try:
            courses.append({'data-course-key': array_course_listing[i]['course_key'], 'course-name': array_course_listing[i]['display_name']})
        except:
            pass
    for i in range(len(array_archive_listing)):
        try:
            courses.append({'data-course-key': array_archive_listing[i]['course_key'], 'course-name': array_archive_listing[i]['display_name']})
        except:
            pass
    return courses

def getCourseStructure(_cms_server,_set_cookie,_locator):
    '''
    connects to the studio server and returns the edx course structure to navigate afterwards
    '''
    url = _cms_server + '/course/' + _locator
    cookies=""
    for key,value in _set_cookie.iteritems():
        cookies = cookies + key + ' = ' + value + ';'
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        'X-CSRFToken': _set_cookie.get('csrftoken', ''),
        'content-type': "application/json; charset=UTF-8",
        'accept-encoding': "gzip, deflate",
        'Referer':'https://studio.edx.org/',
        'accept-language': "es,en;q=0.8,en-US;q=0.6",
        'cookie': cookies,
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers)
    return json.loads(response.text)

def getVerticalChildrens(_cms_server,_set_cookie,_locator):
    '''
    connects to the studio server and get an array of the nodeids that are children of a vertical node
    vertical nodes need to be treated different since its childrens does not show in the course structure
    '''
    url = _cms_server + '/xblock/' + _locator +'/container_preview'
    payload = ''
    cookies=""
    for key,value in _set_cookie.iteritems():
        cookies = cookies + key + ' = ' + value + ';'
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        'X-CSRFToken': _set_cookie.get('csrftoken', ''),
        'content-type': "application/json; charset=UTF-8",
        'accept-encoding': "gzip, deflate",
        'Referer':'https://studio.edx.org/',
        'accept-language': "es,en;q=0.8,en-US;q=0.6",
        'cookie': cookies,
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers)
    result = response.text.decode('utf-8')
    verticalHtml = html.fromstring(json.loads(result)['html'])
    blockCSS = CSSSelector('li.studio-xblock-wrapper')
    blocks = blockCSS(verticalHtml)
    blockIds = []
    for block in blocks:
        blockIds.append(block.attrib['data-locator'])
    return blockIds

def getNodeData(_cms_server,_set_cookie,_locator):
    '''
    takes the data of a xblock node
    '''
    url = _cms_server +'/xblock/' + _locator
    payload = ''
    cookies=""
    for key,value in _set_cookie.iteritems():
        cookies = cookies + key + ' = ' + value + ';'
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        'X-CSRFToken': _set_cookie.get('csrftoken', ''),
        'content-type': "application/json; charset=UTF-8",
        'accept-encoding': "gzip, deflate",
        'Referer':'https://studio.edx.org/',
        'accept-language': "es,en;q=0.8,en-US;q=0.6",
        'cookie': cookies,
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers)
    return json.loads(response._content)



def addNode(_cms_server,_set_cookie,_parentKey,_category,_nodeName):
    '''
    inserts s new node hanging of the parentNode assigned as parameter, we can set the node category and display_name
    '''
    url = _cms_server + "/xblock/"
    payload = "{\"parent_locator\":\""+ _parentKey +"\",\"category\":\""+ _category +"\",\"display_name\":\"" + _nodeName + "\"}"
    cookies=""
    for key,value in _set_cookie.iteritems():
        cookies = cookies + key + ' = ' + value + ';'
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        'X-CSRFToken': _set_cookie.get('csrftoken', ''),
        'content-type': "application/json; charset=UTF-8",
        'accept-encoding': "gzip, deflate",
        'Referer':'https://studio.edx.org/',
        'accept-language': "es,en;q=0.8,en-US;q=0.6",
        'cookie': cookies,
        'cache-control': "no-cache",
        }
    '''
    "_gat=1;_gali=instructor-dashboard-content;__unam=6becc6c-152cabc8dd6-5a48c9f2-33;optimizelySegments=%7B%221759980731%22%3A%22gc%22%2C%221767210027%22%3A%22false%22%2C%221770560429%22%3A%22referral%22%2C%222207441788%22%3A%22none%22%2C%222300020266%22%3A%22true%22%2C%222667650315%22%3A%22true%22%7D;optimizelyBuckets=%7B%225244453691%22%3A%225230184353%22%2C%225263281104%22%3A%225282240148%22%2C%225535331506%22%3A%225541091235%22%7D;AWSELB=D1EF6B6510E347E5B895826CD53CF4FD55E0CFA9A9B17C67E997749A7CB1057C1D42C22E09C81635A14DBECFFC1B42310A6C79432C583EAE591F65FD084E6693F1009EDC31;_cb_ls=1;ajs_anonymous_id=%2220c025ac-a6a2-4092-a534-1c1b3cbff5f9%22;_ga=GA1.2.1830449883.1455100296;ajs_group_id=null;ajs_user_id=%223298730%22;_cb=DY3oa7CNrO0eDVxDv2;_chartbeat2=.1457519395371.1479800907788.0000000000000011.Dw76jUClFHydCYDX9CCFfT0_SFkOF;_chartbeat5=44,758,%2Fcourse%2FUPValenciaX%2FBI101x%2F2T2015,https%3A%2F%2Fstudio.edx.org%2Fcourse%2FUPValenciaX%2FBI101x%2F2T2015,IESnBQMLB0CdNyg5CVG_GRCM9Yc0,*%5B%40id%3D'content'%5D%2Fdiv%5B2%5D%2Fsection%5B1%5D%2Farticle%5B1%5D%2Fdiv%5B2%5D%2Farticle%5B1%5D%2Fdiv%5B1%5D%2Fol%5B1%5D%2Fli%5B2%5D%2Fdiv%5B3%5D%2Fdiv%5B1%5D%2Fa%5B1%5D,c,CYcQR0Ci9_sUCLEfvSD4U-pWtp5YD,studio.edx.org;__utma=201676869.1830449883.1455100296.1479733294.1479733294.1;__utmb=201676869.10.9.1479806971054;__utmc=201676869;__utmz=201676869.1479733294.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);__utmt=1;; edxloggedin=true; prod-edx-sessionid=" +_set_cookie.get('sessionid', '')+ '; prod-edx-user-info='+ _set_cookie.get('edx-user-info', '')  +'; csrftoken='+ _set_cookie.get('csrftoken', '')
    '''
    response = requests.request("POST", url, data=str(payload), headers=headers)
    return json.loads(response.text)

def delNode(_cms_server,_set_cookie,_locator):
    '''
    :param _cms_server:
    :param _set_cookie:
    :param _locator:
    :return:

    deletes a node from an studio based on its locator ( a node can be a course or an html file )
    '''
    url = _cms_server + "/xblock/" + _locator

    payload =""
    cookies=""
    for key,value in _set_cookie.iteritems():
        cookies = cookies + key + ' = ' + value + ';'
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        'X-CSRFToken': _set_cookie.get('csrftoken', ''),
        'content-type': "application/json; charset=UTF-8",
        'accept-encoding': "gzip, deflate",
        'Referer':'https://studio.edx.org/',
        'accept-language': "es,en;q=0.8,en-US;q=0.6",
        'cookie': cookies,
        'cache-control': "no-cache",
    }

    response = requests.request("DELETE", url, data=payload, headers=headers)
    return json.loads(response.text)

def updateNode(_cms_server, _set_cookie,_locator,_coursekey,_category,_displayname,_data,_metadata):
    '''
    Updates the node data and display_name of a node (this way we can fill the node data of inserted nodes)
    :param _cms_server:
    :param _set_cookie:
    :param _locator:
    :param _coursekey:
    :param _category:
    :param _displayname:
    :param _data:
    :return:
    '''
    url  = _cms_server + "/xblock/" + _locator
    payload = "{\"id\":\""+ _locator +"\",\"courseKey\":\""+ _coursekey +"\",\"category\":\""+ _category +"\",\"display_name\":\""+ _displayname +"\",\"data\":\""+ _data.replace('\n','\\n').replace('"','\\"') +"\",\"metadata\":" + json.dumps(_metadata) + ",\"studio_url\":null,\"child_info\":null,\"ancestor_info\":null,\"edited_on\":null,\"edited_by\":null,\"published\":null,\"published_on\":null,\"published_by\":null,\"has_changes\":null,\"visibility_state\":null,\"released_to_students\":null,\"release_date\":null,\"release_date_from\":null,\"currently_visible_to_students\":null,\"due_date\":null,\"format\":null,\"course_graders\":null,\"graded\":null,\"start\":null,\"due\":null,\"has_explicit_staff_lock\":null,\"ancestor_has_staff_lock\":null,\"staff_lock_from\":null,\"staff_only_message\":null,\"has_content_group_components\":null,\"actions\":null,\"is_header_visible\":null,\"explanatory_message\":null,\"group_access\":null,\"user_partitions\":null}"
    cookies=""
    for key,value in _set_cookie.iteritems():
        cookies = cookies + key + ' = ' + value + ';'

    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        'X-CSRFToken': _set_cookie.get('csrftoken', ''),
        'content-type': "application/json; charset=UTF-8",
        'accept-encoding': "gzip, deflate",
        'Referer':'https://studio.edx.org/',
        'accept-language': "es,en;q=0.8,en-US;q=0.6",
        'cookie': cookies,
        'cache-control': "no-cache",
        }

    response = requests.request("POST", url, data=str(payload), headers=headers)
    return json.loads(response.text)

def copyNode (cmsServerSource,cookiesSource,cmsServerTarget,cookiesTarget,nodeTarget,nodeSource):
    '''
    Copys a node from one server as a child of another node in another server
    :param cmsServerSource:
    :param cookiesSource:
    :param cmsServerTarget:
    :param cookiesTarget:
    :param nodeTarget:
    :param nodeSource:
    :return:
    '''
    parentLocator = addNode(cmsServerTarget,cookiesTarget,nodeTarget,nodeSource['category'],nodeSource['display_name'])
    if 'child_info' in nodeSource:
        for children in nodeSource['child_info']['children']:
            copyNode (cmsServerSource,cookiesSource,cmsServerTarget,cookiesTarget,parentLocator['locator'],children)
    elif nodeSource['category'] == 'vertical':
        blocks = getVerticalChildrens(cmsServerSource,cookiesSource,nodeSource['id'])
        for block in blocks:
            nodeData = getNodeData(cmsServerSource,cookiesSource,block)
            copyNode(cmsServerSource,cookiesSource,cmsServerTarget,cookiesTarget,parentLocator['locator'],nodeData)
    if 'data' in nodeSource:
        updateNode(cmsServerTarget,cookiesTarget,parentLocator['locator'],parentLocator['courseKey'],nodeSource['category'],nodeSource['display_name'],nodeSource['data'],nodeSource['metadata'])


def main():
    #exampleussage
    '''
    we have a settings.py file wich defines the server source/target connections of each one of our servers below an example of that file
    SERVERS = [
        {
            'name':'edxorg',
            'url_lms':'https://courses.edx.org',
            'url_studio': 'https://studio.edx.org',
            'user': 'example.admin@edx.org',
            'password': 'example'
        }    ,
        {
            'name':'upvxtest',
            'url':'https://upvx.es',
            'url_studio': 'https://studio.upvx.es',
            'user':'example.admin@upv.es',
            'password':'example'
        }
    ]
    :return:
    '''
    COURSESOURCELOCATOR='course-v1:UPValenciaX+BSP101x+1T2017'

    serverSource = (server for server in settings.SERVERS if server["id"] == "edxorg").next()
    #login into the source server
    cookiesSource = logIn(serverSource['url_lms'],serverSource['url_studio'],serverSource['user'],serverSource['password'])
    #get a list of courses in the source server
    coursesSource = getCourses(serverSource['url_studio'],cookiesSource)
    pdb.set_trace()
    courseSource = getCourseStructure(serverSource['url_studio'], cookiesSource, COURSESOURCELOCATOR)
    pdb.set_trace()
    '''
    #we chose the first course in the list as source course (for this example purpose)
    #courseSource = getCourseStructure(serverSource['url_studio'],cookiesSource,COURSESOURCELOCATOR)
    #we chose the first chapter of the selected course to make a duplicate
    #chapterSource = courseSource['child_info']['children'][CHAPTERSOURCEVALUE]
    #login into the target server
    #pdb.set_trace()
    #cookiesTarget = logIn(serverTarget['url_lms'],serverTarget['url_studio'],serverTarget['user'],serverTarget['password'])
    #get a list of courses into the target server
    #coursesTarget = getCourses(serverTarget['url_studio'],cookiesTarget)
    #for this example we will insert the chapter in the first course of the course list coursesTarget[0]['data-course-key']
    #courseTarget = getCourseStructure(serverTarget['url_studio'],cookiesTarget,COURSETARGETLOCATOR)
    #cross your fingers... (if u have defined correctly both servers u should have a copy of the first chapter of the first course of the serverSource
    #into the first course of the server target
    print serverSource['url_studio']
    print cookiesSource
    print serverTarget['url_studio']
    print cookiesTarget
    print courseTarget['id']
    print chapterSource
    #copyNode(serverSource['url_studio'],cookiesSource,serverTarget['url_studio'],cookiesTarget,courseTarget['id'],chapterSource)
    '''
main()