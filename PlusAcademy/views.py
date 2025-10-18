from django.shortcuts import render,redirect
from .models import Course,Lesson, Messages,CustomUser
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()

def home(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'PlusAcademy/index.html', context)


def courses(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'PlusAcademy/Courses.html', context)


@login_required(login_url='login')
def manage_courses_lessons(request):
    lessons = Lesson.objects.all()
    courses = Course.objects.all()
    return render(request, 'PlusAcademy/courses/manage_courses_lessons.html', {'lessons': lessons, 'courses': courses})


@login_required(login_url='login')
def add_courses(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        course = Course(title=title, description=description, image=image)
        course.save()
        return redirect('home')

    return render(request, 'PlusAcademy/courses/manage_courses_lessons.html')


@login_required(login_url='login')
def add_lesson(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        title = request.POST.get('title')
        description = request.POST.get('description')
        video = request.FILES.get('video')
        attachment = request.FILES.get('attachment')

        lesson = Lesson(course_id=course_id, title=title, description=description, video=video, attachment=attachment)
        lesson.save()

        return redirect('course_detail', course_id=course_id)
    return render(request, 'PlusAcademy/courses/manage_courses_lessons.html', {'courses': Course.objects.all()})


# تعديل كورس
@login_required(login_url='login')
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        if request.FILES.get('image'):
            course.image = request.FILES.get('image')
        course.save()
        return redirect('manage')
    return render(request, 'PlusAcademy/courses/update_course.html', {'course': course})


# حذف كورس
@login_required(login_url='login')
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('manage')


# تعديل درس
@login_required(login_url='login')  
def update_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        lesson.course_id = request.POST.get('course')
        lesson.title = request.POST.get('title')
        lesson.description = request.POST.get('description')
        if request.FILES.get('video'):
            lesson.video = request.FILES.get('video')
        if request.FILES.get('attachment'):
            lesson.attachment = request.FILES.get('attachment')
        lesson.save()
        return redirect('manage')
    return render(request, 'PlusAcademy/courses/update_lesson.html', {'lesson': lesson, 'courses': Course.objects.all()})
    

# حذف درس
@login_required(login_url='login')
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    return redirect('manage')


def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, 'PlusAcademy/courses/course_detail.html', context)


@login_required(login_url='login')
def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    context = {
        'lesson': lesson
    }
    return render(request, 'PlusAcademy/courses/lesson_detail.html', context)


@login_required(login_url='login')
def lesson_attachment(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if lesson.attachment:
        return FileResponse(lesson.attachment.open(), as_attachment=True)
    else:
        return HttpResponse("لا يوجد مرفق لهذا الدرس.")


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject= request.POST.get('subject')
        message = request.POST.get('message')
        Messages.objects.create(
            name=name, 
            phone=phone, 
            email=email, 
            subject=subject, 
            message=message
        )
        messages.success(request, "تم استلام رسالتك بنجاح، سنعاود التواصل قريبًا.")
        return redirect('home')
    return render(request, 'PlusAcademy/contact.html')


def messages_list(request):
    messages = Messages.objects.all().order_by('-created_at')
    return render(request, 'PlusAcademy/messages_list.html', {'messages': messages})


@login_required(login_url='login')
def profile(request):
    return render(request, 'PlusAcademy/profile/profile.html')


@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")

        if request.FILES.get("profile_pic"):
            user.profile_pic = request.FILES["profile_pic"]

        user.save()
        messages.success(request, "✅ تم تحديث الملف الشخصي بنجاح")
        return redirect("profile")

    return render(request, "PlusAcademy/profile/edit_profile.html")


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, "❌ تم حذف الحساب بنجاح")
    return redirect("home")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "تم تسجيل الدخول بنجاح.")
            return redirect('home')
        else:
            messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
            return render(request, 'PlusAcademy/login/login.html')
    return render(request, 'PlusAcademy/login/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "تم تسجيل الخروج بنجاح.")
    return redirect('home')


def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        profile_pic = request.FILES.get('profile_pic')

        # هنا تقدر تضيف أي حقول إضافية تحتاجها

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        user.phone = phone
        user.profile_pic = profile_pic
        user.save()
        
        messages.success(request, "تم إنشاء الحساب بنجاح.")
        return redirect('login')
    return render(request, 'PlusAcademy/login/create_user.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # التحقق من كلمة المرور القديمة
        if not request.user.check_password(old_password):
            messages.error(request, "❌ كلمة المرور القديمة غير صحيحة")
            return render(request, 'PlusAcademy/login/change_password.html')

        # التحقق من تطابق الكلمتين
        if new_password1 != new_password2:
            messages.error(request, "❌ كلمتا المرور غير متطابقتين")
            return render(request, 'PlusAcademy/login/change_password.html')

        # تحديث كلمة المرور
        request.user.set_password(new_password1)
        request.user.save()

        # مهم جدًا: تحديث الجلسة علشان ما يتعملش تسجيل خروج أوتوماتيك
        update_session_auth_hash(request, request.user)

        messages.success(request, "✅ تم تغيير كلمة المرور بنجاح.")
        return redirect('home')

    return render(request, 'PlusAcademy/login/change_password.html')


def reset_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # بدل ما نبعث ايميل هنحوّل المستخدم مباشرة لصفحة إدخال كلمة مرور جديدة
            return redirect('reset_password_confirm', user_id=user.id)
        except User.DoesNotExist:
            messages.error(request, "❌ البريد الإلكتروني غير مسجل لدينا.")
            return render(request, 'PlusAcademy/login/reset_password_request.html')

    return render(request, 'PlusAcademy/login/reset_password_request.html')


def reset_password_confirm(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "❌ المستخدم غير موجود.")
        return render(request, 'PlusAcademy/login/reset_password_request.html')

    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 != new_password2:
            messages.error(request, "❌ كلمتا المرور غير متطابقتين")
            return render(request, 'PlusAcademy/login/reset_password_confirm.html', {'user': user})

        # تحديث كلمة المرور
        user.set_password(new_password1)
        user.save()

        return redirect('login')

    return render(request, 'PlusAcademy/login/reset_password_confirm.html')

