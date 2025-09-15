from django.shortcuts import render, get_object_or_404
from .models import Course, Chapter, Topic, Quiz
from django.http import JsonResponse


def home(request):
    """Asosiy landing page"""
    return render(request, "index.html")


def course_content(request, topic_id=None):
    course = Course.objects.first()
    chapters = course.chapters.all()  # type: ignore

    selected_topic = None
    if topic_id:
        selected_topic = get_object_or_404(Topic, id=topic_id)
    else:
        # agar hech narsa tanlanmagan bo‘lsa, 1-mavzuni default olamiz
        first_chapter = chapters.first()
        if first_chapter:
            selected_topic = first_chapter.topics.first()
    topic_id = selected_topic.id # type: ignore
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

    return render(
        request,
        "quiz.html",
        {
            "quiz": quiz,
            "questions": questions
        },
    )
