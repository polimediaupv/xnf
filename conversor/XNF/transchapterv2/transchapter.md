#serversrc edxtest.cc.upv.es
#coursesrc 574d7f4c8211cb04f0cb6ccb
#chaptersrc 3474a735e7ad488480611ac1fd6fad56

#serverdst edxtest.cc.upv.es
#coursedst 5757d6048211cb0bcde04a41
'''
when we create a chapter at
http://edxtest.cc.upv.es:18010/xblock/
we need the parent locator, category, and display name
course parent locator has the form block-v1:{org}+{course}+{run}+type@course+block@course

{"parent_locator":"block-v1:leosamu+tranchapter_tests001+2016_002+type@course+block@course","category":"chapter","display_name":"SecciÃ³n"}

it will answer with the chapter locator and courseKey
{
  "locator": "block-v1:leosamu+tranchapter_tests001+2016_002+type@chapter+block@e3cb10ddfbb540caaf57a722b912c026",
  "courseKey": "course-v1:leosamu+tranchapter_tests001+2016_002"
}
'''
#copyChapter('edxtest.cc.upv.es','block-v1:leosamu tranchapter_tests001 2016_002 type@course block@course',u'37803bc1704140329ccb041cf8039752','edxtest.cc.upv.es','block-v1:leosamu+transchapterreceiver+2016_002+type@course+block@course')

#EDX_HOMEPAGE = 'http://edxtest.cc.upv.es/'
#LOGIN_API = 'http://edxtest.cc.upv.es/user_api/v1/account/login_session/'
#DASHBOARD = 'http://edxtest.cc.upv.es:18010/home/'

