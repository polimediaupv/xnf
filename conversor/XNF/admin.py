from django.contrib import admin
from models import TranslateCourseStatus
from models import Alert

class TranslateCourseStatusAdmin(admin.ModelAdmin):
    list_display=('courseId','type','fileId','filePath','status','startDate','lastUpdate')

class AlertAdmin(admin.ModelAdmin):
    list_display=('user','viewed','type','msg','url','startDate')

admin.site.register(Alert, AlertAdmin)
admin.site.register(TranslateCourseStatus, TranslateCourseStatusAdmin)