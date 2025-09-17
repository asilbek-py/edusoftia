from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("course-content/", views.course_content, name="course_content"),
    path("course/topic/<int:topic_id>/", views.course_content, name="course_topic"),
    path("topic/<int:topic_id>/next/", views.next_topic_view, name="next_topic"),
    
    path("quiz/<int:chapter_id>/", views.quiz_view, name="quiz_view"),
    path("quiz/<int:quiz_id>/submit/", views.submit_quiz, name="submit_quiz"),
    
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
