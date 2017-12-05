# coding=utf-8
__author__ = 'leosamu'
__author__ = u"Leonardo Salom Muñoz"
__credits__ = u"Leonardo Salom Muñoz"
__version__ = u"0.0.1-SNAPSHOT"
__maintainer__ = u"Leonardo Salom Muñoz"
__email__ = u"leosamu@upv.es"
__status__ = u"Development"
'''
before we update the production server we need to fix chapter and sequential start dates
'''

import pymongo
import bson.son
from django.core.management.base import BaseCommand, CommandError


#server = "edxtest.cc.upv.es"
DEFAULTSTARTDATE = '2047-03-24T00:00:00Z'
connection = None
db = None
modulestore = None

class Command(BaseCommand):
    help = 'Fixes the course startdates in a mongo server'
    def handle(self, *args, **options):
        for server in options['server']:
            fixStartDates(server)


def fixStartDates(server):
    createconnection(server)
    startdate = None
    #find all courses
    dbCourses = modulestore.find({'_id.category': 'course'})
    for course in dbCourses:
        if 'metadata' in course.keys():
            if 'start' in course['metadata'].keys():
                startdate = course['metadata']['start']
            else:
                #if course with no start date we set it to javi and leo retirement maxdate
                startdate = DEFAULTSTARTDATE
                id = bson.son.SON([('tag',course['_id']['tag']),('org', course['_id']['org']), ('course', course['_id']['course']),('category',course['_id']['category']),('name', course['_id']['name']),('revision',course['_id']['revision'])])
                course['metadata']['start']=startdate
                modulestore.update({'_id':id},{'$set':{'metadata':course['metadata']}},upsert=True)
        else:
            startdate = DEFAULTSTARTDATE
            id = bson.son.SON([('tag',course['_id']['tag']),('org', course['_id']['org']), ('course', course['_id']['course']),('category',course['_id']['category']),('name', course['_id']['name']),('revision',course['_id']['revision'])])
            modulestore.update({'_id':id},{'$set':{'metadata':{'start':startdate}}},upsert=True)
        fixChildren(course,startdate)


def fixChildren(_node,_startdate):
    if 'definition' in _node.keys() and 'children' in _node['definition'].keys():
        for i in range (len(_node['definition']['children'])):
            start = _startdate
            children = getnode(_node['definition']['children'][i])
            #we only fix start date in chapters and sequentials
            if children !=None:
                if children['_id']['category'] =='chapter' or children['_id']['category'] =='sequential':
                    if 'metadata' in children.keys() and 'start' in children['metadata'].keys() and children['metadata']['start']!="" and children['metadata']['start']!=None:
                        start = children['metadata']['start']
                    else:
                        id = bson.son.SON([('tag',children['_id']['tag']),('org', children['_id']['org']), ('course', children['_id']['course']),('category',children['_id']['category']),('name', children['_id']['name']),('revision',children['_id']['revision'])])
                        if 'metadata' in children.keys():
                            children['metadata']['start']=start
                            modulestore.update({'_id':id},{'$set':{'metadata':children['metadata']}},upsert=True)
                        else:
                            modulestore.update({'_id':id},{'$set':{'metadata':{'start':start}}},upsert=True)
                    fixChildren(children,start)
            else:
                print "cant find node " +_node['definition']['children'][i]

def getnode(_strnode):
    nodesplit = _strnode.split('/')
    node = modulestore.find_one({'_id.org': nodesplit[2], '_id.category': nodesplit[4], '_id.course': nodesplit[3], '_id.name': nodesplit[5]})
    return node

def createconnection(server):
    global connection
    global db
    global modulestore
    connection = pymongo.Connection("mongodb://" + server, safe=True)
    db = connection.edxapp
    modulestore = db.modulestore



