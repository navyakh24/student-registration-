from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_app/list.html', {'students': students})


@login_required(login_url='/login/')
def add_student(request):   # ✅ ADD LOGIN REQUIRED (important)
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'student_app/add.html', {'form': form})   # ✅ FIXED TEMPLATE


@login_required(login_url='/login/')
def update_student(request, id):
    std = get_object_or_404(Student, id=id)   # ✅ safer
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=std)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=std)

    return render(request, 'student_app/update.html', {'form': form})


@login_required(login_url='/login/')
def delete_student(request, id):
    std = get_object_or_404(Student, id=id)   # ✅ safer
    std.delete()
    return redirect('student_list')


def student_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # ✅ CHECK PASSWORD MATCH
        if password != confirm_password:
            return render(request, 'student_app/register.html', {
                'error': 'Passwords do not match'
            })

        # ✅ CHECK USER EXISTS
        if User.objects.filter(username=username).exists():
            return render(request, 'student_app/register.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(username=username, password=password)
        return redirect('student_login')   # ✅ FIXED NAME

    return render(request, 'student_app/register.html')


def student_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ HANDLE ?next=
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            return redirect('student_list')
        else:
            return render(request, 'student_app/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'student_app/login.html')


def student_logout_view(request):
    logout(request)
    return redirect('student_login')   # ✅ FIXED