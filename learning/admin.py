from django.contrib import admin
from .models import Course, Chapter, Topic, Quiz, Question, Choice, UserProgress, QuizAttempt


class ChapterInline(admin.TabularInline):
    """Kurs ichida bo'limlarni tezda qo'shish uchun"""
    model = Chapter
    extra = 1


class TopicInline(admin.TabularInline):
    """Bo'lim ichida mavzularni qo'shish"""
    model = Topic
    extra = 1


class ChoiceInline(admin.TabularInline):
    """Savol ichida variantlarni ko'rsatish"""
    model = Choice
    extra = 2


class QuestionInline(admin.TabularInline):
    """Quiz ichida savollarni tezda qo'shish"""
    model = Question
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)
    inlines = [ChapterInline]


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title",)
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "chapter", "order")
    list_filter = ("chapter",)
    search_fields = ("title", "content")


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "chapter", "pass_score")
    list_filter = ("chapter",)
    search_fields = ("title", "description")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz", "order")
    list_filter = ("quiz",)
    search_fields = ("text",)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct", "question")
    search_fields = ("text",)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "topic", "completed")
    list_filter = ("completed", "user")
    search_fields = ("user__username", "topic__title")


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "passed", "attempt_date")
    list_filter = ("passed", "quiz", "attempt_date")
    search_fields = ("user__username", "quiz__title")
    ordering = ("-attempt_date",)
