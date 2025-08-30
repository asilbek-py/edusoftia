from django.shortcuts import render, get_object_or_404
from .models import Course, Chapter, Topic, Quiz

def home(request):
    """Asosiy landing page"""
    return render(request, "index.html")

def course_content(request):
    """Kurs bo'limlari va mavzularni chiqaradi"""
    course = Course.objects.first()
    chapters = course.chapters.all() # type: ignore
    return render(request, "course_content.html", {
        "course": course,
        "chapters": chapters
    })

def topic_detail(request, topic_id):
    """Alohida mavzu sahifasi"""
    topic = get_object_or_404(Topic, id=topic_id)
    return render(request, "topic_detail.html", {
        "topic": topic
    })

def quiz_view(request, chapter_id):
    """Chapter oxiridagi quiz"""
    quiz = get_object_or_404(Quiz, chapter_id=chapter_id)
    return render(request, "quiz.html", {
        "quiz": quiz,
        "questions": quiz.questions.all() # type: ignore
    })
