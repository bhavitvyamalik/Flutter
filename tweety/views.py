from django.shortcuts import render

# retrieve
def home(request):
	return render(request,"home.html",{})
