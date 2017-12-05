#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os, pprint, sys, math, urllib,urllib2, cookielib, shutil, json,re
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import sys
import settings
import pdb

reload(sys)
sys.setdefaultencoding('utf8')



def logIn(server):
    #Get Token
    pdb.set_trace()
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    response = opener.open('http://' + server + '/')
    set_cookie = {}
    for cookie in cj:
        set_cookie[cookie.name] = cookie.value
    #Prepare Headers
    headers = {'User-Agent': 'edX-downloader/0.01',
               'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
               'Referer': 'http://' + server + '/',
               'X-Requested-With': 'XMLHttpRequest',
               'X-CSRFToken': set_cookie.get('csrftoken', '') }

    #Login
    post_data = urllib.urlencode({
                'email' : settings.user_email,
                'password' : settings.user_pswd,
                'remember' : False
                }).encode('utf-8')
    request = urllib2.Request('http://' + server +'/user_api/v1/account/login_session/', post_data,headers)
    response = urllib2.urlopen(request)
    '''resp = json.loads(response.read().decode(encoding = 'utf-8'))
    if not resp.get('success', False):
        print 'Wrong Email or Password.'
        exit(2)
    '''
    #Get user info/courses
    opener.open('http://' + server +':18010/home/')
    for cookie in cj:
        set_cookie[cookie.name] = cookie.value

    return set_cookie

def addNode(server,_set_cookie,_parentKey,_category,_nodeName):
    url = "http://" + server + ":18010/xblock/"
    payload = "{\"parent_locator\":\""+ _parentKey +"\",\"category\":\""+ _category +"\",\"display_name\":\"" + _nodeName + "\"}"
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        'X-CSRFToken': _set_cookie.get('csrftoken', ''),
        'content-type': "application/json; charset=UTF-8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "es,en;q=0.8,en-US;q=0.6",
        'cookie': 'video_player_volume_level=100; complianceCookie=True; _ga=GA1.2.223453357.1454512420; TDP=qpObrHh17SyoryG7YYxL31s74669; UPV_IDIOMA=es; __utma=253516877.223453357.1454512420.1464164284.1464333627.36; __utmc=253516877; __utmz=253516877.1464164284.35.26.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); T=foto1; edxloggedin=true; sessionid=' +_set_cookie.get('sessionid', '')+ '; edx-user-info='+ _set_cookie.get('edx-user-info', '')  +'; csrftoken='+ _set_cookie.get('csrftoken', ''),
        'cache-control': "no-cache",
        }

    response = requests.request("POST", url, data=str(payload), headers=headers)
    return response

def delNode(_set_cookie,_locator):
    url = "http://edxtest.cc.upv.es:18010/xblock/" + _locator

    payload =""

    headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    'x-csrftoken': _set_cookie.get('csrftoken', ''),
    'accept-encoding': "gzip, deflate, sdch",
    'accept-language': "es,en;q=0.8,en-US;q=0.6",
    'cookie': 'video_player_volume_level=100; complianceCookie=True; _ga=GA1.2.223453357.1454512420; TDP=qpObrHh17SyoryG7YYxL31s74669; UPV_IDIOMA=es; __utma=253516877.223453357.1454512420.1464164284.1464333627.36; __utmc=253516877; __utmz=253516877.1464164284.35.26.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); T=foto1; edxloggedin=true; sessionid=' +_set_cookie.get('sessionid', '')+ '; edx-user-info='+ _set_cookie.get('edx-user-info', '')  +'; csrftoken='+ _set_cookie.get('csrftoken', ''),
    'cache-control': "no-cache",
    }

    response = requests.request("DELETE", url, data=payload, headers=headers)
    return response

def updateNode(_server,_set_cookie,_locator,_coursekey,_category,_displayname,_data):
    url  = "http://" + _server + ":18010/xblock/" + _locator
    payload = "{\"id\":\""+ _locator +"\",\"courseKey\":\""+ _coursekey +"\",\"category\":\""+ _category +"\",\"display_name\":\""+ _displayname +"\",\"data\":\""+ _data.replace('\n','\\n').replace('"',"'") +"\",\"metadata\":{},\"studio_url\":null,\"child_info\":null,\"ancestor_info\":null,\"edited_on\":null,\"edited_by\":null,\"published\":null,\"published_on\":null,\"published_by\":null,\"has_changes\":null,\"visibility_state\":null,\"released_to_students\":null,\"release_date\":null,\"release_date_from\":null,\"currently_visible_to_students\":null,\"due_date\":null,\"format\":null,\"course_graders\":null,\"graded\":null,\"start\":null,\"due\":null,\"has_explicit_staff_lock\":null,\"ancestor_has_staff_lock\":null,\"staff_lock_from\":null,\"staff_only_message\":null,\"has_content_group_components\":null,\"actions\":null,\"is_header_visible\":null,\"explanatory_message\":null,\"group_access\":null,\"user_partitions\":null}"

    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        'X-CSRFToken': _set_cookie.get('csrftoken', ''),
        'content-type': "application/json; charset=UTF-8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "es,en;q=0.8,en-US;q=0.6",
        'cookie': 'video_player_volume_level=100; complianceCookie=True; _ga=GA1.2.223453357.1454512420; TDP=qpObrHh17SyoryG7YYxL31s74669; UPV_IDIOMA=es; __utma=253516877.223453357.1454512420.1464164284.1464333627.36; __utmc=253516877; __utmz=253516877.1464164284.35.26.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); T=foto1; edxloggedin=true; sessionid=' +_set_cookie.get('sessionid', '')+ '; edx-user-info='+ _set_cookie.get('edx-user-info', '')  +'; csrftoken='+ _set_cookie.get('csrftoken', ''),
        'cache-control': "no-cache",
        }

    response = requests.request("POST", url, data=str(payload), headers=headers)
    return response

def main():
    cookies = logIn()
    response = addNode(cookies,'block-v1:leosamu+transchapterreceiver+2016_002+type@course+block@course','chapter','prueba')
    print response.text
    response = delNode(cookies,json.loads(response.text)['locator'])
    response = updateNode(cookies,'locator','coursekey','category','Nuevo html','<p>prueba de update22</p>')
    print response.text

#main()