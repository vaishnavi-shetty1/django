from django.shortcuts import render,redirect,get_object_or_404
from .models import Students
from .forms import StudentForm

def student_list(request):
    students =Students.objects.all()
    return render(request,'student/student_list.html',{'students':students})

def add_student(request):
    form=StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request,'student/student_form.html',{'form':form})

def update_student(request,id): 
    student = get_object_or_404(Students,id=id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request,'student/student_form.html',{'form':form})
    
def delete_student(request,id):
    student = get_object_or_404(Students,id=id)
    student.delete()
    return redirect('student_list')
    
    