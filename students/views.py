from django.shortcuts import render, redirect
from .models import Student, Attendance
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# 🔐 REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # ✅ Check passwords match
        if password != confirm_password:
            return render(request, 'register.html', {
                'error': 'Passwords do not match'
            })

        # ✅ Check user exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'User already exists'
            })

        # ✅ Create user
        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'register.html')


# 🔐 LOGIN
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')


# 🔓 LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')


# 📊 DASHBOARD
@login_required
def dashboard(request):
    today = date.today()

    total_students = Student.objects.count()
    present_today = Attendance.objects.filter(date=today, status=True).count()
    absent_today = total_students - present_today

    percentage = (present_today / total_students * 100) if total_students else 0

    return render(request, 'dashboard.html', {
        'total_students': total_students,
        'present_today': present_today,
        'absent_today': absent_today,
        'percentage': percentage
    })


# 📅 MARK ATTENDANCE
@login_required
def mark_attendance(request):
    students = Student.objects.all()

    if request.method == "POST":
        for student in students:
            status = request.POST.get(str(student.id)) == "on"

            Attendance.objects.create(
                student=student,
                date=date.today(),
                status=status
            )

        return redirect('view_attendance')

    return render(request, 'mark.html', {'students': students})


# 📊 VIEW ATTENDANCE (WITH FILTER)
@login_required
def view_attendance(request):
    students = Student.objects.all()
    data = []

    selected_date = request.GET.get('date')

    for student in students:
        records = Attendance.objects.filter(student=student)

        if selected_date:
            records = records.filter(date=selected_date)

        total = records.count()
        present = records.filter(status=True).count()

        percentage = (present / total * 100) if total else 0

        data.append({
            'name': student.name,
            'percentage': percentage
        })

    return render(request, 'view.html', {
        'data': data,
        'selected_date': selected_date
    })