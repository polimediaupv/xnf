# -*- coding: utf-8 -*-
from django import forms
from django.template.defaultfilters import filesizeformat
import os

IMPORT_FILE_TYPES = ['.xls','.xlsm' ]
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "20971520"


class DocumentForm(forms.Form):
    input_excel = forms.FileField(
        label=u"""
        """,
        help_text='Estamos en fase de pruebas',
        widget=forms.FileInput(attrs={'class' : 'hiddenbutton', 'onchange':'convert()'}),
    )

    def clean_input_excel(self):
        input_excel = self.cleaned_data['input_excel']
        extension = os.path.splitext( input_excel.name )[1]
        #if input_excel._size > int(MAX_UPLOAD_SIZE):
        #        raise forms.ValidationError(_(u'Por favor manten el tamaño de los archivos por debajo de %s. Tamaño del archivo actual %s') % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(input_excel._size)))
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError( u'%s no es un archivo de excel válido. Asegurese de enviar un archivo de excel.' % extension )
        else:
            if input_excel.size > int(MAX_UPLOAD_SIZE):
                raise forms.ValidationError(u'Por favor manten el tamaño de los archivos por debajo de %s. Tamaño del archivo actual %s' % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(input_excel.size)))
            else:
                return input_excel

class edxTarForm(forms.Form):
    input_excel = forms.FileField(
        label=u"""
        """,
        help_text='Estamos en fase de pruebas',
        widget=forms.FileInput(attrs={'class' : 'hiddenbutton', 'onchange':'convert()'}),
    )

    def clean_input_excel(self):
        input_tar = self.cleaned_data['input_tar']
        extension = os.path.splitext( input_excel.name )[1]
        #if input_excel._size > int(MAX_UPLOAD_SIZE):
        #        raise forms.ValidationError(_(u'Por favor manten el tamaño de los archivos por debajo de %s. Tamaño del archivo actual %s') % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(input_excel._size)))
        if not (extension == 'tar.gz'):
            raise forms.ValidationError( u'%s no es un archivo de curso válido. Asegurese de enviar un archivo de targz.' % extension )
        else:
            if input_excel.size > int(MAX_UPLOAD_SIZE):
                raise forms.ValidationError(u'Por favor manten el tamaño de los archivos por debajo de %s. Tamaño del archivo actual %s' % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(input_excel.size)))
            else:
                return input_excel

