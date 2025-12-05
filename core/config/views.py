from django.shortcuts import render

# Create your views here.
def maintenance_view(request):
    return render(request, 'config/maintenance.html')