from django.shortcuts import render
from website.forms import ContactForm,NewsletterForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ContactForm, NewsletterForm

class IndexView(TemplateView):
    template_name = 'website/index2.html'

class AboutView(TemplateView):
    template_name = 'website/about2.html'

class NotificationView(TemplateView):
    template_name = 'notification.html'

class ContactView(FormView):
    template_name = 'website/contact2.html'
    form_class = ContactForm
    success_url = reverse_lazy('website:contact')

    def form_valid(self, form):
        obj = form.save(commit=False)
        # obj.name = "anonymous"
        obj.save()
        messages.success(self.request, "ok")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "error")
        return super().form_invalid(form)

class NewsletterView(View):

    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "your email registered")
        else:
            messages.error(request, "error in your email")
        return HttpResponseRedirect('/')

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')


# def index_view(request):
#     return render(request,'website/index2.html')

# def about_view(request):
#     return render(request,'website/about2.html')

# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             obj = form.save(commit = False)
#             obj.name = "anonymous"
#             obj.save()
#             messages.add_message(request,messages.SUCCESS,"ok")
#         else: 
#             messages.add_message(request,messages.ERROR,"error")
#         return HttpResponseRedirect('contact') 
       
#     form = ContactForm()
#     context = {'form':form}
#     return render(request,'website/contact2.html',context)

# def notification_view(request):
#     return render(request,'notification.html')

# def newsletter_view(request):
#     if request.method == 'POST':
#         form = NewsletterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.add_message(request,messages.SUCCESS,"your email registered")
#         else: 
#             messages.add_message(request,messages.ERROR,"error in your email")
#         return HttpResponseRedirect('/') 
#     else: 
#         return HttpResponseRedirect('/')
    