from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from . import models
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model
User = get_user_model()

#for selecting corresponding foreign key models
from braces.views import SelectRelatedMixin
from django.http import Http404
from django.contrib import messages

class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user','group')

class UserPost(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact = self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user','group')
    template_name = 'posts/post_detail.html'

    # def get_queryset(self):
    #     query_set = super().get_queryset()
    #     query_set = query_set.filter(user__username__iexact = self.kwargs.get('username'))
    #     print(query_set)
    #     return query_set 

class CreatePost(LoginRequiredMixin,generic.CreateView,SelectRelatedMixin):
    model = models.Post
    fields = ('message','group')
    
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    
class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        quert_set = super().get_queryset()
        return quert_set.filter(user_id = self.request.user.id)
    
    def delete(self,*args,**kwargs):
        messages.success(self.request, 'Post deleted')
        return super().delete(*args,**kwargs)