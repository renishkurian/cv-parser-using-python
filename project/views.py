import os
import random
import string

import PyPDF2
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string

from project.form import NewProject
from rework.settings import MEDIA_URL, MEDIA_ROOT
from .models import Project as pro, FileBin, Project, FolderColor, Cvbin, cvcombination, Cvgroups

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, FormView


class FilterCreate(CreateView):
    model = Cvbin
    fields = ['bucketname']


@login_required
def get_bucket(request):
    result = ''
    try:
        combination, bin, project = request.POST.get('id').split('/')
        combination, bin, project = request.POST.get('id').split('/')
        selected_project = Project.objects.get(id=project, owner=request.user)
        cvbin_object = Cvbin.objects.get(id=bin, project=selected_project)
        combo = cvcombination.objects.get(bin_id=cvbin_object, id=combination)
        print(combo.id)
        result = Cvgroups.objects.select_related('cv').filter(combination=combo)

    except:

        pass

    return JsonResponse({'result':render_to_string('project/cv_list.html',{'result':result}),'combo':combo.combo.title()})


def create_bucket(request):
    if request.method == "POST":
        seleted = Project.objects.get(id=request.POST.get('pk'), owner=request.user)
        if seleted:
            bucket = Cvbin()
            bucket.project = seleted
            bucket.bucketname = request.POST.get('filter')
            bucket.save()

    return redirect(request.META.get('HTTP_REFERER'))


class Projects(LoginRequiredMixin, ListView):
    model = pro
    context_object_name = 'projects'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('foldercolor')
        return queryset.filter(is_deleted=0)


class ProjectInfo(LoginRequiredMixin, DetailView):
    model = pro
    ordering = ['-created_at']

    def post(self, request, *args, **kwargs):
        seleted = Project.objects.get(id=request.POST.get('pk'), owner=request.user)
        if seleted:
            files = request.FILES.getlist('cv')
            for f in files:
                cv = FileBin()
                cv.project = seleted
                cv.filename = f.name
                cv.path = f
                cv.save()


        else:
            print("not found")

        return redirect(request.path)


def delete(request):
    if request.method == 'POST':
        print("**post**")
        data = request.POST.get('id')
        seleted = Project.objects.get(id=data, owner=request.user)
        seleted.is_deleted = 1;
        seleted.save()
        foldername = seleted.id
        data = {
            'message': f'{seleted.name} Deleted',
            'status': 1

        }
        if not seleted:
            data = {
                'message': 'Not Deleted',
                'status': 0

            }

            return JsonResponse(data)

        return JsonResponse(data)
    else:
        return redirect('/')


def folder_color(request):
    if request.is_ajax():
        seleted = Project.objects.get(id=request.POST.get('id'), owner=request.user)
        print(seleted.id)

        if seleted:
            folder, created = FolderColor.objects.get_or_create(parent=seleted,
                                                                defaults={'color': request.POST.get('color')})

            if not created:
                folder.color = request.POST.get('color')
                folder.save()

    data = {
        'message': f'{seleted.name} color changed',
        'status': 1

    }

    return JsonResponse(data)


class CreateNewProject(FormView):
    form_class = NewProject
    template_name = 'project/FileBin_form.html'
    success_url = '/project/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('cv')
        if form.is_valid():
            newproject = Project()
            newproject.name = request.POST.get("title", "")
            newproject.owner = request.user
            newproject.save()
            import PyPDF2

            for f in files:
                cv = FileBin()
                cv.project = newproject
                cv.filename = f.name
                cv.path = f
                cv.save()
                fname = MEDIA_ROOT + '/' + str(cv.path)
                pdf = open(fname, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdf)

                # printing number of pages in pdf file
                cv.page = pdfReader.numPages
                cv.save()

                ...  # Do something with each file.

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # if request.method=='POST':
    #     newproject=Project()
    #     newproject.name=request.POST.get("title", "")
    #     newproject.owner=request.user
    #     newproject.save()
    #
    # return render(request,'project/FileBin_form.html')


def test(r):
    return HttpResponse(1)
