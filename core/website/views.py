from django.shortcuts import render
from website.forms import ContactForm,NewsletterForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.
def index_view(request):
    return render(request,'website/index2.html')

def about_view(request):
    return render(request,'website/about2.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.name = "anonymous"
            obj.save()
            messages.add_message(request,messages.SUCCESS,"ok")
        else: 
            messages.add_message(request,messages.ERROR,"error")
        return HttpResponseRedirect('contact') 
       
    form = ContactForm()
    context = {'form':form}
    return render(request,'website/contact2.html',context)

def notification_view(request):
    return render(request,'notification.html')

def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"your email registered")
        else: 
            messages.add_message(request,messages.ERROR,"error in your email")
        return HttpResponseRedirect('/') 
    else: 
        return HttpResponseRedirect('/')
    