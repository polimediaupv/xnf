# -*- coding: utf-8 -*-
from django.db import models
from django import forms

class Document(models.Model):
    #docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    uploaded_file = forms.FileField(required=False)



class TranslateCourseStatus(models.Model):
    courseId = models.CharField(max_length = 200,default=None)
    fileId = models.CharField(max_length = 200)
    filePath =  models.CharField(max_length = 200)
    srcLang = models.CharField(max_length = 200)
    trgLang = models.CharField(max_length = 200)
    startDate = models.DateTimeField(auto_now=False,auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True,auto_now_add=True)
    numErrors = models.IntegerField(max_length=1)
    user = models.CharField(max_length = 200)

    displayName =  models.CharField(max_length = 350)
    displayNameTrg =  models.CharField(max_length = 350)

    TRANSLATION_TYPE = (
        (1, 'TITLE'),
        (2, 'BODY')
    )

    TRANSLATION_STATUS =(
        (0,'Started'),
        (1,'Uploaded'),
        (2,'Translated'),
        (3,'Retrieved'),
        (4,'Completed')
    )

    type = models.IntegerField(max_length=1,choices=TRANSLATION_TYPE)
    status = models.IntegerField(max_length=1,choices=TRANSLATION_STATUS)

    @classmethod
    def create(cls,user,type,courseId,fileId,filePath,srcLang,trgLang):
        coursestatus = cls(type=type,courseId=courseId,fileId=fileId,filePath=filePath,numErrors=0,status=0,srcLang=srcLang,trgLang=trgLang,user=user)
        return coursestatus

class Alert(models.Model):
    user = models.CharField(max_length = 200,default=None)
    viewed = models.BooleanField()
    msg =  models.CharField(max_length = 200)
    url = models.CharField(max_length = 200)
    startDate = models.DateTimeField(auto_now=True,auto_now_add=True)

    ALERT_TYPE =(
        (0,'Default'),
        (1,'Success'),
        (2,'Warning'),
        (3,'Error')
    )

    type = models.IntegerField(max_length=1,choices=ALERT_TYPE)


    @classmethod
    def create(cls,type,user,msg,url):
        alert = cls(type=type,user=user,msg=msg,url=url,viewed=False)
        return alert