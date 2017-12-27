from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView

from .mixin import FormsUserNeededMixin,UserOwnerMixin
from .forms import TweetModelForm
from .models import Tweet

# Create

class TweetCreateView(CreateView,FormsUserNeededMixin):
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
    success_url=reverse_lazy("tweet:list")  #/tweet/list/

# List / Search

#Retrieve
class TweetDetailView(DetailView):
    queryset=Tweet.objects.all()

class TweetListView(ListView):
    def get_queryset(self,*args,**kwargs):
        qs=Tweet.objects.all()
        query=self.request.GET.get("q",None)
        if query is not None:
            qs=qs.filter(
                Q(content__icontains=query)|
                Q(user__username__icontains=query)
                )
        return qs

    def get_context_data(self,*args,**kwargs):
        context=super(TweetListView,self).get_context_data(*args,**kwargs)
        return context