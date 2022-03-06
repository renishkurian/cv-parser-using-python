import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.timezone import now


class Project(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=0)

    def __str__(self):
        return self.name


def get_member_upload_to(instance, filename):
    new_filename = '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1])
    return "cvbin/{}/{}/{}".format(instance.project.owner.username, instance.project.name, new_filename)


class FileBin(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    filename = models.CharField(max_length=256, null=True)
    path = models.FileField(upload_to=get_member_upload_to)
    page = models.IntegerField(default=0)
    content = models.TextField(default='')
    file_hash = models.CharField(max_length=256, default=0)
    is_delted = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=12, null=True)
    email = models.CharField(max_length=256, null=True)
    applicant = models.CharField(max_length=256, null=True)
    cv_updated=models.CharField(max_length=256,null=True)

    class Meta:
        ordering = ["-created_at"]


class Cvbin(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    bucketname = models.CharField(max_length=256)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
class  cvcombination(models.Model):
    bin_id=models.ForeignKey(Cvbin,on_delete=models.CASCADE)
    combo=models.CharField(max_length=256, null=True)
    is_delted = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class Cvgroups(models.Model):
    combination = models.ForeignKey(cvcombination, on_delete=models.CASCADE,null=True)
    cv=models.ForeignKey(FileBin,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.cv.filename


class FolderColor(models.Model):
    parent = models.OneToOneField(Project, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
