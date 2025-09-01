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
    """Har bir bo'lim uchun test"""

    chapter = models.OneToOneField(
        Chapter, related_name="quiz", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    pass_score = models.PositiveIntegerField(default=50)  # foiz

    def __str__(self):
        return f"Quiz: {self.title}"


class Question(models.Model):
    """Savollar"""

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text[:50]


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
