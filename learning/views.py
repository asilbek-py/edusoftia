from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Course,
    Chapter,
    Topic,
    Quiz,
    Question,
    Choice,
    QuizAttempt,
    UserProgress,
)
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
        first_chapter = chapters.first()
        if first_chapter:
            selected_topic = first_chapter.topics.first()

    if not selected_topic:
        return redirect("course_content")

    # === Progress hisoblash ===
    total_topics = Topic.objects.count()
    completed_topics = UserProgress.objects.filter(
        user=request.user, completed=True
    ).count()
    topic_progress = (
        round((completed_topics / total_topics) * 100, 1) if total_topics > 0 else 0
    )

    total_quizzes = Quiz.objects.count()
    completed_quizzes = (
        QuizAttempt.objects.filter(user=request.user, passed=True)
        .values("quiz")
        .distinct()
        .count()
    )
    quiz_progress = (
        round((completed_quizzes / total_quizzes) * 100, 1) if total_quizzes > 0 else 0
    )
    current_topic = selected_topic
    completed_topic_ids = UserProgress.objects.filter(
        user=request.user, completed=True
    ).values_list("topic_id", flat=True)

    return render(
        request,
        "course_content.html",
        {
            "course": course,
            "chapters": chapters,
            "selected_topic": selected_topic,
            "current_topic": current_topic,
            "topic_progress": topic_progress,
            "completed_topics": completed_topics,
            "total_topics": total_topics,
            "quiz_progress": quiz_progress,
            "completed_quizzes": completed_quizzes,
            "total_quizzes": total_quizzes,
            "completed_topic_ids": list(completed_topic_ids),
        },
    )


@login_required(login_url="login")
def next_topic_view(request, topic_id):
    current_topic = get_object_or_404(Topic, id=topic_id)

    # ✅ Progress update
    progress, created = UserProgress.objects.get_or_create(
        user=request.user, topic=current_topic
    )
    if not progress.completed:
        progress.completed = True
        progress.save()

    # ✅ Faqat shu chapter ichidagi keyingi topicni olish
    next_topic = (
        Topic.objects.filter(chapter=current_topic.chapter, id__gt=current_topic.id)
        .order_by("id")
        .first()
    )

    if next_topic:
        return redirect("course_topic", topic_id=next_topic.id)
    else:
        # Chapter oxiri bo‘lsa, kurs sahifasiga qaytaradi
        return redirect("course_content")


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    return JsonResponse({"title": topic.title, "content": topic.content})


@login_required(login_url="login")
def quiz_view(request, chapter_id):
    """Savollarni chiqaradi"""
    quiz = get_object_or_404(Quiz, chapter_id=chapter_id)

    questions = []
    for qq in quiz.quiz_questions.select_related("question").all():
        question = qq.question
        questions.append(
            {
                "id": question.id,
                "text": question.text,
                "choices": question.choices.all(),
            }
        )

    return render(request, "quiz.html", {"quiz": quiz, "questions": questions})


@login_required(login_url="login")
def submit_quiz(request, quiz_id):
    """Natijani hisoblaydi"""
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == "POST":
        correct_count = 0
        total_questions = quiz.quiz_questions.count()

        for qq in quiz.quiz_questions.select_related("question"):
            q = qq.question
            selected_choice_id = request.POST.get(f"question_{q.id}")
            if selected_choice_id:
                choice = Choice.objects.filter(
                    id=selected_choice_id, question=q
                ).first()
                if choice and choice.is_correct:
                    correct_count += 1

        score = (
            int((correct_count / total_questions) * 100) if total_questions > 0 else 0
        )
        passed = score >= quiz.pass_score

        QuizAttempt.objects.create(
            user=request.user, quiz=quiz, score=score, passed=passed
        )

        # Natijani shu quiz.html'ning o'zida modal orqali ko'rsatamiz
        questions = []
        for qq in quiz.quiz_questions.select_related("question").all():
            question = qq.question
            questions.append(
                {
                    "id": question.id,
                    "text": question.text,
                    "choices": question.choices.all(),
                }
            )

        return render(
            request,
            "quiz.html",
            {
                "quiz": quiz,
                "questions": questions,
                "score": score,
                "passed": passed,
                "correct_count": correct_count,
                "total_questions": total_questions,
                "show_result": True,
            },
        )

    return redirect("quiz", chapter_id=quiz.chapter_id)


def register(request):
    """Ro'yxatdan o'tish"""
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")  # ✅ endi username ishlatamiz
        phone_number = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("password_confirm")

        if password != confirm_password:
            return render(
                request, "auth/register.html", {"error": "Passwords do not match."}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request, "auth/register.html", {"error": "Username already taken."}
            )

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
        username = request.POST.get("username")  # ✅ username
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
