from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.db.models.signals import post_save

@receiver(post_save,sender=User)
def prof_created(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save,sender=User)
def prof_save(sender,instance,**kwargs):

    instance.profile.save()
