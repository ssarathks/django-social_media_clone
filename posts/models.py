from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

import misaka

from groups.models import Group
# Create your models here.
#POST MODELS



User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(blank=True,default='')
    group = models.ForeignKey(Group, related_name='posts',null=True, blank=True)

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse("posts:for_user", kwargs={"username": self.user.username})
    
    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ('user','message')