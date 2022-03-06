from django import forms
from django.forms import ModelForm

from .models import Project,FileBin

class BookForm(ModelForm):
    class Meta:
        model = FileBin
        fields = ['path', 'project']

class NewProject(forms.Form):
    title=forms.CharField( widget=forms.TextInput(attrs={'class': "form-control col-md-4"}))
    cv=forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))