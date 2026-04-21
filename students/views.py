from django.shortcuts import render, redirect
from .models import Student, Attendance
from datetime import date, datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# 🔐 REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'User already exists'
            })

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
    selected_date = request.GET.get('date')

    if selected_date:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = date.today()

    students = Student.objects.all()
    total_students = students.count()

    records = Attendance.objects.filter(date=selected_date)

    # ✅ avoid duplicate counting
    present_today = records.filter(status=True).values('student').distinct().count()
    absent_today = total_students - present_today

    percentage = (present_today / total_students * 100) if total_students else 0

    return render(request, 'dashboard.html', {
        'total_students': total_students,
        'present_today': present_today,
        'absent_today': absent_today,
        'percentage': round(percentage, 2),
        'selected_date': selected_date
    })


# 📅 MARK ATTENDANCE
from datetime import date, datetime  # ✅ FIXED import

@login_required
def mark_attendance(request):
    students = Student.objects.all().order_by('id')  # optional but cleaner

    if request.method == "POST":
        selected_date = request.POST.get('date')

        # ✅ Safe date handling
        try:
            if selected_date:
                selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
            else:
                selected_date = date.today()
        except ValueError:
            selected_date = date.today()

        for student in students:
            # ✅ checkbox fix
            status = request.POST.get(f"student_{student.id}") == "on"

            Attendance.objects.update_or_create(
                student=student,
                date=selected_date,
                defaults={'status': status}
            )

        return redirect('view_attendance')

    return render(request, 'mark.html', {
        'students': students,
        'selected_date': date.today()
    })


# 📊 VIEW ATTENDANCE (WITH FILTER)
@login_required
def view_attendance(request):
    students = Student.objects.all()
    data = []

    selected_date = request.GET.get('date')

    if selected_date:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    for student in students:
        records = Attendance.objects.filter(student=student)

        if selected_date:
            records = records.filter(date=selected_date)

        total = records.count()
        present = records.filter(status=True).count()

        percentage = (present / total * 100) if total else 0

        data.append({
            'name': student.name,
            'percentage': round(percentage, 2)
        })

    return render(request, 'view.html', {
        'data': data,
        'selected_date': selected_date
    })