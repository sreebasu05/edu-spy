from django.shortcuts import render
from .forms import *
from account.models import *
# Create your views here.
def add_course(request):
    if request.method == 'POST':
        fm = CourseForm(request.POST)
        if fm.is_valid():
            instance = fm.save(commit=False)
            instance.save()
            return render(request,'principal/home.html')
            # return render(request,'teacher/home.html')
        else:
            messages.error(request, 'Please enter valid details')
            return render(request,'principal/home.html')
    else:
        fm=CourseForm()
        return render(request,'principal/create_course.html',{'form':fm})
