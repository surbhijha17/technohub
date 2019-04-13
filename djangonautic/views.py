from django.http import HttpResponse
from django.shortcuts import render
from contact.forms import ContactForm
from articles.models import Category,Article
def homepage(request):
    categories=Category.objects.all()
    articles=Article.objects.all()[:3]
   
    if request.method=='POST':
    	form=ContactForm(request.POST )
    	if form.is_valid():
    		form.save()
    else:
    	form=ContactForm()

    return render(request,"home.html",{'form':form,'categories':categories,'articles':articles})
def about(request):
    #return HttpResponse('hey!!! this is surbhi ')
    return render(request,"about.html")
