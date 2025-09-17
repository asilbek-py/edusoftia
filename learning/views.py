from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Chapter, Topic, Quiz
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


def home(request):
    """Asosiy landing page"""
    return render(request, "index.html")


@login_required(login_url="login")
def course_content(request, topic_id=None):
    course = Course.objects.first()
    chapters = course.chapters.all()  # type: ignore

    selected_topic = None
    if topic_id:
        selected_topic = get_object_or_404(Topic, id=topic_id)
    else:
        # agar hech narsa tanlanmagan bo'lsa, 1-mavzuni default olamiz
        first_chapter = chapters.first()
        if first_chapter:
            selected_topic = first_chapter.topics.first()
    topic_id = selected_topic.id  # type: ignore
    topic = get_object_or_404(Topic, id=topic_id)
    return render(
        request,
        "course_content.html",
        {
            "course": course,
            "chapters": chapters,
            "selected_topic": selected_topic,
            "current_topic": topic,
        },
    )


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    return JsonResponse({"title": topic.title, "content": topic.content})


@login_required(login_url="login")
def quiz_view(request, chapter_id):
    """Chapter oxiridagi quiz"""
    quiz = get_object_or_404(Quiz, chapter_id=chapter_id)

    # quiz ichidagi savollarni tartib bilan olish
    questions = []
    for qq in quiz.quiz_questions.select_related("question").all():
        question = qq.question
        questions.append({
            "id": question.id,
            "text": question.text,
            "choices": question.choices.all()
        })
    context = {
            "quiz": quiz,
            "questions": questions
        }
        
    return render(request, "quiz.html", context=context)


def register(request):
    """Ro'yxatdan o'tish"""
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")   # ✅ endi username ishlatamiz
        phone_number = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("password_confirm")

        if password != confirm_password:
            return render(request, "auth/register.html", {"error": "Passwords do not match."})

        if User.objects.filter(username=username).exists():
            return render(request, "auth/register.html", {"error": "Username already taken."})

        # Foydalanuvchini yaratish
        user = User.objects.create_user(username=username, password=password)
        user.first_name = full_name
        user.save()

        messages.success(request, "Registration successful. Please log in.")
        return redirect("login")

    return render(request, "auth/register.html")


def login_view(request):
    """Login qilish (username + password)"""
    if request.method == "POST":
        username = request.POST.get("username")   # ✅ username
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("course_content")
        else:
            return render(request, "login.html", {"error": "Invalid credentials."})

    return render(request, "auth/login.html")


def logout_view(request):
    """Logout qilish"""
    logout(request)
    return redirect("login")
