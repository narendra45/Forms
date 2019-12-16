from django.http import HttpResponse
from django.shortcuts import render
from .models import UrlTypes

# Create your views here.
def viewAll(request):
    s = UrlTypes.objects.all()
    return render(request,'viewall.html',{'data':s})


def viewDetails(request,id):
    print(id)
    return HttpResponse('This method from  href="/viewdetails/{{ x.id }}"')


def partialUpdate(request):
    id = request.GET['id']
    print(id)
    return HttpResponse('This method from  href="/partialupdate/?id={{ x.id }}"')


def updateDetails(request):
    id = request.GET['id']
    print(id)
    return HttpResponse('This method from href="{% url ''update %}?id={{ x.id }}"')


def deleteDetails(request,id):
    print(id)
    return HttpResponse('href="{% url ''delete x.id %}"')
