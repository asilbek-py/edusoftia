from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("course/", views.course_content, name="course_content"),
    path("course/topic/<int:topic_id>/", views.course_content, name="course_topic"),
    path("chapter/<int:chapter_id>/quiz/", views.quiz_view, name="quiz_view"),
    path("quiz/<int:chapter_id>/", views.quiz_view, name="quiz_detail")
]
