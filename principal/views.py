from django.shortcuts import render
from .forms import *
from django.contrib import messages
from account.models import *
# Create your views here.
def add_course(request):
    if request.method == 'POST':
        fm = CourseForm(request.POST)
        if fm.is_valid():
            instance = fm.save(commit=False)
            instance.save()

            i = instance.id
            curr_course = Course.objects.get(pk = i)
            batches = Batch.objects.filter(in_class = curr_course.class_no)
            for b in batches:
                BatchCourse.objects.create(
                batch= b,
                course= curr_course,
            ).save()
            messages.success(request,'created')
            return render(request,'principal/home.html')
            # return render(request,'teacher/home.html')
        else:
            messages.error(request, 'Please enter valid details')
            return render(request,'principal/home.html')
    else:
        fm=CourseForm()
        return render(request,'principal/create_course.html',{'form':fm})

def view_courses(request):
    teacher_profile = TeacherProfile.objects.get(teacher= request.user)
    print(teacher_profile.department)
    courses = Course.objects.filter(name= teacher_profile.department)
    print(courses)
    context ={'courses' : courses}
    return render(request,'principal/viewcourses.html',context)

def completedetails_course(request,id):
    course = Course.objects.get(pk=id)

    print(course.name)
    units = Unit.objects.filter(course= course)
    context ={'course' : course, 'units' : units}
    return render(request,'principal/completedetails_course.html',context)


def add_unit(request, id):
    c = Course.objects.get(pk=id)
    print(c)
    if request.method == 'POST':
        fm = UnitForm(request.POST)
        if fm.is_valid():

            instance = fm.save(commit=False)
            instance.course = c
            instance.save()
            i=instance.id
            u = Unit.objects.get(pk=i)
            batchcourses = BatchCourse.objects.filter(course = c)
            # print(batchcourses)
            for b in batchcourses:
                TrackProgressBatchCourse.objects.create(
                unit= u,
                batchcourse= b,
            ).save()
            return render(request,'principal/home.html')
        # return render(request,'teacher/home.html')
        else:
            messages.error(request, 'Please enter valid details')
            return render(request,'principal/home.html')
    else:
        fm=UnitForm()
        profile=TeacherProfile.objects.get(teacher=request.user)
        print(profile)
    # form = UnitForm(initial={'course': request.user.teacher.})
        return render(request,'principal/create_unit.html',{'form':fm})
def coursebatchdetails(request):
    profile=TeacherProfile.objects.get(teacher=request.user)
    courses=Course.objects.filter(name=profile.department)
    batchcourse=[]
    for c in courses:
        batchcourse.append(BatchCourse.objects.filter(course=c))

    return render(request,'principal/coursebatchdetails.html',{'batchcourses':batchcourse})



def add_teacherbatch(request,bc):
    if request.method == 'POST':
        fm = TeacherBatchForm(request.POST)
        if fm.is_valid():

            instance = fm.save(commit=False)
            instance.save()
            return render(request,'principal/home.html')
        # return render(request,'teacher/home.html')
        else:
            messages.error(request, 'Please enter valid details')
            return render(request,'principal/home.html')
    else:
        fm=TeacherBatchForm()
        return render(request,'principal/create_teacherbatch.html',{'form':fm})
