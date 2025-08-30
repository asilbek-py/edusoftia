from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("course/", views.course_content, name="course_content"),
    path("topic/<int:topic_id>/", views.topic_detail, name="topic_detail"),
    path("chapter/<int:chapter_id>/quiz/", views.quiz_view, name="quiz_view"),
]
