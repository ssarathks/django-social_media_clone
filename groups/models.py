from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.urlresolvers import reverse
#for using html of texts
import misaka

#for usign custom template tags
from django import template
register = template.Library()

# Create your models here.
#GROUP MODELS

#

#User model to be used as in foreignkey fields
User = get_user_model()

class Group(models.Model):
    name = models.CharField(max_length = 264, unique = True)
    slug = models.SlugField(allow_unicode = True, unique = True)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,blank=True,null=True)
    members = models.ManyToManyField(User, through = 'GroupMember')

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        return super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})
    
    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(Group,related_name = 'memberships')
    user = models.ForeignKey(User, related_name = 'user_groups')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group','user')