from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView

from .mixin import FormsUserNeededMixin,UserOwnerMixin
from .forms import TweetModelForm
from .models import Tweet

class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated():
            new_tweet = Tweet.objects.retweet(request.user, tweet)
            return HttpResponseRedirect("/")
        return HttpResponseRedirect(tweet.get_absolute_url())

# Create

class TweetCreateView(LoginRequiredMixin,CreateView,FormsUserNeededMixin):
    form_class=TweetModelForm
    template_name='tweets/create_view.html'
    #success_url="/tweet/create/"
    #login_url='/admin/'

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(TweetCreateView,self).form_valid(form)

# Update
class TweetUpdateView(UserOwnerMixin,LoginRequiredMixin,UpdateView):
    queryset=Tweet.objects.all()
    form_class=TweetModelForm
    template_name='tweets/update_view.html'
   # success_url="/tweet/"

# Delete
class TweetDeleteView(LoginRequiredMixin,DeleteView):
    model=Tweet
    template_name='tweets/delete_confirm.html'
    success_url=reverse_lazy("tweet:list")                                      #go to tweets/urls.py for more info. You'll find itself. [namespace:urlname]

# List / Search

#Retrieve
class TweetDetailView(DetailView):
    queryset=Tweet.objects.all()

class TweetListView(LoginRequiredMixin,ListView):
    def get_queryset(self,*args,**kwargs):
        qs=Tweet.objects.all()
        query=self.request.GET.get("q",None)
        if query is not None:
            qs=qs.filter(                                                       #looks up things based on filters you've put up. "Making queries" Django
                Q(content__icontains=query)|
                Q(user__username__icontains=query)
                )
        return qs

    def get_context_data(self,*args,**kwargs):
        context=super(TweetListView,self).get_context_data(*args,**kwargs)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy("tweet:create")
        return context
