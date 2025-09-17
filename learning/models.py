from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Course(models.Model):
    """Asosiy o'quv kursi (masalan: Software Construction & Evolution)"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    """Kurs bo'limlari (masalan: Chapter 1 - Introduction)"""
    course = models.ForeignKey(
        Course, related_name="chapters", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Topic(models.Model):
    """Bo'lim ichidagi mavzular (masalan: 1.1 Course Overview)"""
    chapter = models.ForeignKey(
        Chapter, related_name="topics", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    content = RichTextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"


class Quiz(models.Model):
    """Chapter oxiridagi test"""
    chapter = models.ForeignKey(
        Chapter, related_name="quizzes", on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    pass_score = models.PositiveIntegerField(default=50)  # foiz

    def __str__(self):
        return f"{self.id} - {self.title}"


class Question(models.Model):
    """Savollar (bir nechta quiz ichida ishlatilishi mumkin)"""
    text = models.TextField()

    def __str__(self):
        return self.text[:50]


class QuizQuestion(models.Model):
    """Quiz va Question orasidagi bog‘lanish (ko‘pga-ko‘p)"""
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="quiz_questions"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_quizzes"
    )
    order = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("quiz", "question")
        ordering = ["order"]

    def __str__(self):
        return f"{self.quiz.title} ↔ {self.question.text[:30]}"


class Choice(models.Model):
    """Savol variantlari"""
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserProgress(models.Model):
    """Foydalanuvchi qaysi mavzuni o'qib chiqqani"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "topic")

    def __str__(self):
        return f"{self.user.username} - {self.topic.title}"


class QuizAttempt(models.Model):
    """Foydalanuvchi test topshirgani"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    attempt_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} ({self.score}%)"
