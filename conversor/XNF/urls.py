# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('conversor.XNF.views',
    url(r'^report/$', 'report', name='report'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^tmp/$', 'download', name='download'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^conversor/$', 'conversor', name='conversor'),
)


urlpatterns += patterns('conversor.XNF.views',
    url(r'^createnewuser/$', 'createnewuser', name='createnewuser'),
)


urlpatterns += patterns('conversor.XNF.views',
    url(r'^updateprofile/$', 'updateprofile', name='updateprofile'),
)
'''
urlpatterns += patterns('conversor.XNF.views',
    url(r'^conversorM1/$', 'conversorM1', name='conversorM1'),
)



urlpatterns += patterns('conversor.XNF.views',
    url(r'^paellayoutubeviewer/$', 'paellayoutubeviewer', name='paellayoutubeviewer'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^youtubesub/$', 'youtubesub', name='youtubesub'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^attachsubs/$', 'attachsubs', name='attachsubs'),
)



urlpatterns += patterns('conversor.XNF.views',
    url(r'^transchapter/$', 'transchapter', name='transchapter'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^ytapi/$', 'ytapi', name='ytapi'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^copychapter/$', 'copychapter', name='copychapter'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^addsubs/$', 'addsubs', name='addsubs'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^ytmsg/$', 'ytmsg', name='ytmsg'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^edxorggetcourses/$', 'edxorggetcourses', name='edxorggetcourses'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^polimedias/$', 'polimedias', name='polimedias'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^coursetranslate/$', 'coursetranslate', name='coursetranslate'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^coursetranslatedata/$', 'coursetranslatedata', name='coursetranslatedata'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^coursetranslatedetail/$', 'coursetranslatedetail', name='coursetranslatedetail'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^coursetranslatedetaildata/$', 'coursetranslatedetaildata', name='coursetranslatedetail'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^getCourseTranslation/$', 'getCourseTranslation', name='getCourseTranslation'),
)


urlpatterns += patterns('conversor.XNF.views',
    url(r'^imgcrop/$', 'imgcrop', name='imgcrop'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^startTranslate/$', 'startTranslate', name='startTranslate'),
)


'''

urlpatterns += patterns('conversor.XNF.views',
    url(r'^profile/$', 'profile', name='profile'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^newuser/$', 'newuser', name='newuser'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^coursecalendar/$', 'coursecalendar', name='coursecalendar'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^coursesdates/$', 'coursesdates', name='coursesdates'),
)



urlpatterns += patterns('conversor.XNF.views',
    url(r'^transchapterv2/$', 'transchapterv2view', name='transchapterv2view'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^transchapterv2listcourse/$', 'transchapterv2listcourse', name='transchapterv2listcourse'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^transchapterv2listchapters/$', 'transchapterv2listchapters', name='transchapterv2listchapters'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^transchapterv2copychapter/$', 'transchapterv2copychapter', name='transchapterv2copychapter'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^index/$', 'index', name='index'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^startEdx2Xnf/$', 'startEdx2Xnf', name='startEdx2Xnf'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^addCSVconversion/$', 'addCSVconversion', name='addCSVconversion'),
)

urlpatterns += patterns('conversor.XNF.views',
    url(r'^addPoliciesconversion/$', 'addPoliciesconversion', name='addPoliciesconversion'),
)
