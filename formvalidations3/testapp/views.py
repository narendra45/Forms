from django.shortcuts import render

# Create your views here.
from testapp.forms import SignUpForm


def signup_form(request):
    form = SignUpForm()
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('SignUp Is completed and printing Data')
            print('Name:',form.cleaned_data['name'])
            print('Password:',form.cleaned_data['password'])
            print('Email:',form.cleaned_data['email'])
    return render(request,'signup.html',{'form':form})