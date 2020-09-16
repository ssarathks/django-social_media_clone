from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from groups.models import Group,GroupMember
from django.contrib import messages
from django.db import IntegrityError
# Create your views here.


class GroupCreate(LoginRequiredMixin, generic.CreateView):
    model = Group
    fields = ('name','description')

class GroupDetail(generic.DetailView):
    model = Group

class GroupList(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(group = group, user = self.request.user)
        except IntegrityError:
            messages.warning(self.request,('already a member'))
        else:
            messages.success(self.request,('Joined'))
        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,("Member not exist"))
        else:
            membership.delete()
            messages.success(self.request,("leaved"))
        return super().get(request,*args,**kwargs)
