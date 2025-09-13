from django.contrib import admin
from .models import (
    Course, Chapter, Topic,
    Quiz, Question, QuizQuestion, Choice,
    UserProgress, QuizAttempt
)


class TopicInline(admin.TabularInline):
    """Chapter ichida Topiclarni ko‘rsatish"""
    model = Topic
    extra = 1

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("id","title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title", "course__title")
    ordering = ("course", "order")
    inlines = [TopicInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)


class ChoiceInline(admin.TabularInline):
    """Question ichida variantlarni ko‘rsatish"""
    model = Choice
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text",)
    search_fields = ("text",)
    inlines = [ChoiceInline]


class QuizQuestionInline(admin.TabularInline):
    """Quiz ichida Questionlarni ko‘rsatish"""
    model = QuizQuestion
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "pass_score")
    search_fields = ("title",)
    inlines = [QuizQuestionInline]


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "completed")
    list_filter = ("completed", "user")
    search_fields = ("user__username", "topic__title")


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "passed", "attempt_date")
    list_filter = ("passed", "attempt_date", "quiz")
    search_fields = ("user__username", "quiz__title")


# Qo‘shimcha registratsiyalar
admin.site.register(QuizQuestion)